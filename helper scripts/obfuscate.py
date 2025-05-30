import re
import random
import string
import sys

def random_var_name(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def obfuscate_code(source_code):
    # 1. Remove comments (simple single line and inline comments)
    no_comments = re.sub(r'#.*', '', source_code)

    # 2. Remove blank lines
    lines = [line.rstrip() for line in no_comments.splitlines() if line.strip() != '']

    code = '\n'.join(lines)

    # 3. Find variable/function/class names to rename - simplistic approach
    # We'll rename only variables defined with assignment (var = ...), function defs, class defs.
    names = set()

    # Regex to find variables (left side of assignment)
    var_pattern = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=')
    func_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(')
    class_pattern = re.compile(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[:\(]')

    for line in lines:
        var_match = var_pattern.match(line)
        if var_match:
            names.add(var_match.group(1))
        func_match = func_pattern.search(line)
        if func_match:
            names.add(func_match.group(1))
        class_match = class_pattern.search(line)
        if class_match:
            names.add(class_match.group(1))

    # Exclude common keywords or built-in names that you want to keep
    exclude_names = set([
        'app', 'request', 'redirect', 'render_template', 'abort', 'flash', 'url_for',
        'current_user', 'login_user', 'logout_user', 'login_required',
        'bcrypt', 'MongoClient', 'ObjectId', 'cloudinary', 'secrets', 'time', 'requests',
        'UserMixin', 'LoginManager', 'markdown', 'math', 'wraps', 'csv', 'StringIO',
        'secure_filename', 'ServerSelectionTimeoutError', 'json_util'
    ])

    # Filter names to rename
    to_rename = [name for name in names if name not in exclude_names and not name.startswith('__')]

    # Map original names to obfuscated names
    rename_map = {name: random_var_name() for name in to_rename}

    # Replace variable names in code - careful with boundaries to avoid partial replacements
    pattern = re.compile(r'\b(' + '|'.join(re.escape(name) for name in rename_map.keys()) + r')\b')

    def replacer(match):
        return rename_map[match.group(0)]

    obfuscated_code = pattern.sub(replacer, code)

    # 4. Remove extra spaces (multiple spaces to single space)
    obfuscated_code = re.sub(r'[ \t]+', ' ', obfuscated_code)

    return obfuscated_code


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python obfuscate.py input.py output.py")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r', encoding='utf-8') as f:
        source = f.read()

    obf_code = obfuscate_code(source)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(obf_code)

    print(f"Obfuscated code written to {output_file}")
