import sys

def is_table_row(line):
    # Consider it a table row if it has at least one tab
    return '\t' in line.strip('\n')

def format_table_row(line):
    parts = line.strip('\n').split('\t')
    return '| ' + ' | '.join(parts) + ' |'

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    out_lines = []
    in_table = False
    col_count = 0
    
    for line in lines:
        # Ignore empty lines inside a table (sometimes people leave blanks)
        if in_table and line.strip() == '':
            out_lines.append(line)
            in_table = False
            continue
            
        if is_table_row(line):
            parts = line.strip('\n').split('\t')
            if not in_table:
                in_table = True
                col_count = len(parts)
                out_lines.append(format_table_row(line) + '\n')
                # Add separator
                separator = '| ' + ' | '.join(['---'] * col_count) + ' |'
                out_lines.append(separator + '\n')
            else:
                # If column count mismatches, just add empty columns or merge to not break markdown table
                # But for simplicity, just format it with the parts it has
                out_lines.append(format_table_row(line) + '\n')
        else:
            in_table = False
            out_lines.append(line)
            
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)

if __name__ == '__main__':
    process_file('BacklogCaracteristics.md', 'BacklogCaracteristics.md')
    print("Formatting complete.")
