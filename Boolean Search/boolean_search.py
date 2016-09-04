import re


def tokenize(document):
    """ Convert a string representing one document into a list of
    words. Remove all punctuation and split on whitespace.
    Params:
      document...a string to be tokenized
    Returns:
      A list of strings, one per token.
    Here is a doctest:
    >>> tokenize("Hi  there. What's going on?")
    ['hi', 'there', 'what', 's', 'going', 'on']
    """
    ###TODO
    document = str(document).lower()
    return re.findall('\w+', document)



def create_index(tokens):
    """
    Create an inverted index given a list of document tokens. The index maps
    each unique word to a list of document ids, sorted in increasing order.
    Params:
      tokens...A list of lists of strings
    Returns:
      An inverted index. This is a dict where keys are words and values are
      lists of document indices, sorted in increasing order.
    Below is an example, where the first document contains the tokens 'a' and
    'b', and the second document contains the tokens 'a' and 'c'.
    >>> index = create_index([['a', 'b'], ['a', 'c']])
    >>> sorted(index.keys())
    ['a', 'b', 'c']
    >>> index['a']
    [0, 1]
    >>> index['b']
    [0]
    """
    ###TODO
    index_list = {}
    for docid, doc in enumerate(tokens):
        for token in doc:
            if token not in index_list:
                index_list[token] = [docid]
            else:
                index_list[token].append(docid)
    return index_list

def intersect(list1, list2):
    """ Return the intersection of two posting lists. Use the optimize
    algorithm of Figure 1.6 of the MRS text. Your implementation should be
    linear in the sizes of list1 and list2. That is, you should only loop once
    through each list.
    Params:
      list1....A list of document indices, sorted in ascending order.
      list2....Another list of document indices, sorted in ascending order.
    Returns:
      The list of document ids that appear in both lists, sorted in ascending order.
    >>> intersect([1, 3, 5], [3, 4, 5, 10])
    [3, 5]
    >>> intersect([1, 2], [3, 4])
    []
    """
    ###TODO
    intersect_1 = []
    list1_index = 0
    list2_index = 0
    while list1_index < len(list1) and list2_index < len(list2):

        if list1[list1_index] == list2[list2_index]:
            intersect_1.append(list1[list1_index])
            list1_index += 1
            list2_index += 1
        elif list1[list1_index] < list2[list2_index]:
            list1_index += 1
        else:
            list2_index += 1
    return intersect_1




def sort_by_num_postings(words, index):
    """
    Sort the words in increasing order of the length of their postings list in
    index. You may use Python's builtin sorted method.
    Params:
      words....a list of strings.
      index....An inverted index; a dict mapping words to lists of document
      ids, sorted in ascending order.
    Returns:
      A list of words, sorted in ascending order by the number of document ids
      in the index.

    >>> sort_by_num_postings(['a', 'b', 'c'], {'a': [0, 1], 'b': [1, 2, 3], 'c': [4]})
    ['c', 'a', 'b']
    """
    ###TODO
    num_dict = {}
    for word in words:
        num_dict[word] = len(index[word])
    num_dict = sorted(num_dict, key=num_dict.get)

    return num_dict



def search(index, query):
    """ Return the document ids for documents matching the query. Assume that
    query is a single string, possibly containing multiple words. The steps
    are to:
    1. tokenize the query
    2. Sort the query words by the length of their postings list
    3. Intersect the postings list of each word in the query.

    If a query term is not in the index, then an empty list should be returned.

    Params:
      index...An inverted index (dict mapping words to document ids)
      query...A string that may contain multiple search terms. We assume the
      query is the AND of those terms by default.

    E.g., below we search for documents containing 'a' and 'b':
    >>> search({'a': [0, 1], 'b': [1, 2, 3], 'c': [4]}, 'a b')
    [1]
    """
    ###TODO

    token_query = tokenize(query)
    token = sort_by_num_postings(token_query, index)

    if len(token) == 0:
        return []
    if len(token) == 1:
        return index[token[0]]
    elif len(token_query) == 2:
        i = intersect(index[token[0]], index[token[1]])
        return i
    else:
        a = 0
        j = intersect(index[token[a]], index[token[a+1]])
        a += 1
        while a+1 > len(token_query):
            if j == []:
                return j
            else:
                intersect(j, index[token[a+1]])
                a += 1
    return j






def main():
    """ Main method. You should not modify this. """
    documents = open('documents.txt').readlines()
    tokens = [tokenize(d) for d in documents]
    index = create_index(tokens)
    queries = open('queries.txt').readlines()
    for query in queries:
        results = search(index, query)
        print('\n\nQUERY:%s\nRESULTS:\n%s' % (query, '\n'.join(documents[r] for r in results)))


if __name__ == '__main__':
    main()

