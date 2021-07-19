import re

'''
    Probably the least efficient way of converting a Java file to JSP
    But hey, it works! ;)

    Will NOT work for all formats of Java files
    Refer the sample.java file for some details
'''

java_file_path = "sample.java"


def find_closing_braces(text, open_pos):
    close_pos = open_pos
    counter = 1
    while (counter > 0):
        close_pos += 1
        c = text[close_pos]
        if (c == '{'):
            counter += 1
        elif (c == '}'):
            counter -= 1

    return close_pos

def java_to_jsp(java_file):
    jsp_file = ""

    # Remove the 'package' line
    java_file = re.sub('package.*;', '', java_file, 1)

    # Convert imports
    # Read line-by-line until 'public class' hit
    start_idx = 0
    new_line = re.compile('\n')
    # Challenge: Is there any worse way you could do this? XP
    for _ in range(100):
        new_line_idx = new_line.search(java_file, start_idx).end()
        if new_line_idx - start_idx < 2:
            start_idx = new_line_idx
            continue
        line = java_file[start_idx:new_line_idx-2]
        start_idx = new_line_idx
        if "public class" in line:
            break
        if "import" not in line:
            continue
        jsp_file += "<%@page " + line.replace('import ','import="') + '"%>\n'
    jsp_file += '\n\n\n'

    # Copy main method
    main_idx = java_file.find('public static void main(', new_line_idx)
    main_open_idx = java_file.find('{', main_idx)
    main_close_idx = find_closing_braces(java_file, main_open_idx)
    jsp_file += "<%\n" + java_file[main_open_idx+1:main_close_idx] + "\n%>"

    # Copy variables at the top
    static_block = java_file[new_line_idx:main_idx]

    # Copy remaining methods
    closing_idx = java_file.rindex('}')
    static_block += "\n\n" + java_file[main_close_idx+1:closing_idx]

    if len(static_block.strip()) != 0:
        # Insert the static block
        jsp_file += "\n\n\n<%!\n" + static_block + "\n%>"

    # Change System prints to out
    jsp_file = jsp_file.replace("System.out.println(", "out.print(")
    jsp_file = jsp_file.replace("System.out.print(", "out.print(")

    return jsp_file


if __name__ == "__main__":

    with open(java_file_path, 'r') as java_file:
        jsp_file = java_to_jsp(java_file.read())

    with open('output.jsp', 'w') as out:
        out.write(jsp_file)