import re
import os

def multiple_replace(dict, text):
  # Create a regular expression  from the dictionary keys
  regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

  # For each match, look-up corresponding value in dictionary
  return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 

def createPath(curr_subdir):
    """[summary]

    Args:
        curr_subdir ([type]): [description]
    """
    if not os.path.exists(curr_subdir):
        os.makedirs(curr_subdir, exist_ok=True)
        print(curr_subdir + " directory was made")