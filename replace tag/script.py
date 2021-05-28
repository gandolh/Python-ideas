import csv
file_names = ['train.txt', 'validation.txt']
csv_names = ['train.csv', 'validation.csv']  # order is important!
for filename in file_names:
    with open(filename, encoding='utf-8') as txtfile:
        with open(csv_names[file_names.index(filename)], mode='w', encoding='utf-8') as csv_file:
            csv_file.write('')
            all_text = txtfile.read()
            while('|<start of text>|' in all_text):
                text_between_tags = ''
                text_between_tags = all_text[all_text.find('|<start of text>|')
                                             + 17:all_text.find('|<end of text>|')]
                all_text = all_text[all_text.find(
                    '|<end of text>|') + 15:-1] + all_text[-1]
                with open(csv_names[file_names.index(filename)], mode='a', encoding='utf-8') as csv_file:
                    fieldnames = ['text']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({'text': text_between_tags})
