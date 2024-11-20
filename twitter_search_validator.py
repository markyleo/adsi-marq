import re

class TwitterSearchValidator:
    def __init__(self, search_query):
        self.search_query = search_query
        self.operators = self.parse_search_query(search_query)

    def parse_search_query(self, query):
        """
        Parses the search query and returns a structured representation of operators.
        Handles AND, OR, NOT operators, exact phrases, hashtags, accounts, and mentions.
        """
        exact_phrases = re.findall(r'\"([^\"]+)\"', query)  # Matches exact phrases
        or_blocks = re.findall(r'\((.*?)\)', query)  # Matches content inside OR blocks (parentheses)
        hashtags = re.findall(r'#(\w+)', query)  # Matches hashtags
        exclude_keywords = re.findall(r'-\"([^\"]+)\"|-([\w\u4E00-\u9FFF]+)', query)  # Matches excluded keywords (e.g., -"word" or -word)
        
        # Flatten exclude_keywords to a single list
        exclude_keywords = [kw for sublist in exclude_keywords for kw in sublist if kw]

        from_accounts = [account.lower() for account in re.findall(r'from:(\w+)', query)]
        to_accounts = [account.lower() for account in re.findall(r'to:(\w+)', query)]
        mentioned_accounts = [account.lower() for account in re.findall(r'@(\w+)', query)]

        all_words = re.findall(r'\b\w+\b', re.sub(r'\(.*?\)|[#@]\w+|from:\w+|to:\w+|-\"[^\"]+\"|-\w+', '', query))

        operator_structure = {
            'all_words': [word for word in all_words if word not in exclude_keywords],
            'exact_phrases': [phrase for phrase in exact_phrases if phrase not in exclude_keywords],
            'any_of_these_words': [
                keyword.strip() for block in or_blocks for keyword in block.split(' OR ') 
                if keyword.strip() not in exclude_keywords
            ],
            'none_of_these_words': exclude_keywords,
            'hashtags': hashtags,
            'from_accounts': from_accounts,
            'to_accounts': to_accounts,
            'mentioning_accounts': mentioned_accounts
        }

        return operator_structure

    def validate_post(self, post):
        """
        Validates a post (entire dataset entry) against the parsed operators from the search query.
        Returns True if the post matches the query, False otherwise.
        """
        post_description_lower = post['content'].lower()

        # 1. Validate "From these accounts" (username)
        if self.operators['from_accounts']:
            if post['username'].lower() not in self.operators['from_accounts']:
                return False  # If the post's author isn't in the 'from' accounts list, it's invalid

        # 2. Validate "To these accounts" (inReplyToUsername)
        if self.operators['to_accounts']:
            if post['inReplyToUsername'].lower() not in self.operators['to_accounts']:
                return False

        # 3. Validate "Mentioning these accounts" (mentions)
        if self.operators['mentioning_accounts']:
            if not any(mention.lower() in self.operators['mentioning_accounts'] for mention in post.get('mentions', [])):
                return False  # If none of the mentioned accounts are in 'mention' list, post is invalid

        # 4. Validate "All of these words" (AND condition)
        for word in self.operators['all_words']:
            if word.lower() not in post_description_lower:
                return False  # If any required word is missing, post is invalid

        # 5. Validate "This exact phrase"
        for phrase in self.operators['exact_phrases']:
            if phrase.lower() not in post_description_lower:
                return False  # If an exact phrase is missing, post is invalid

        # 6. Validate "Any of these words" (OR condition)
        if self.operators['any_of_these_words']:
            if not any(keyword.lower() in post_description_lower for keyword in self.operators['any_of_these_words']):
                return False  # If none of the OR group keywords are present, post is invalid

        # 7. Validate "None of these words" (NOT condition)
        for exclude_word in self.operators['none_of_these_words']:
            if exclude_word.lower() in post_description_lower:
                return False  # If any excluded keyword is present, post is invalid

        # 8. Validate hashtags
        for hashtag in self.operators['hashtags']:
            if f"#{hashtag.lower()}" not in post_description_lower:
                return False  # If any required hashtag is missing, post is invalid

        return True  # Post passed all validation checks