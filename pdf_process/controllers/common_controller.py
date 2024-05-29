import json


def json_dump(result_list, json_path):
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(result_list, json_file, ensure_ascii=False, indent=4)


def json_load(json_path):
    with open(json_path, "r", encoding="utf-8") as json_file:
        cleaning_result_table_text_dict = json.load(json_file)
        return cleaning_result_table_text_dict


def txt_dump(file_path, before_txt, result_pdf_txt, after_txt=None):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(before_txt)
        for item in result_pdf_txt:
            null_count = sum(1 for text in list(item.values()) if text == [""])
            if 0 < null_count < 2:
                for sub_idx, (key, value) in enumerate(item.items()):
                    convert_text = [v[0].replace("\n", "") for v in list(item.values())]
                    if sub_idx == 0:
                        file.write(
                            f"{convert_text[sub_idx+1]}: {', '.join(convert_text[sub_idx+2:])}\n"
                        )
                    elif sub_idx != 0:
                        file.write(
                            "{} {}: {}\n".format(
                                key.replace("\n", ""),
                                convert_text[sub_idx + 1],
                                " ".join(convert_text[sub_idx + 2 :]),
                            )
                        )

                    break
            else:
                for key, value in item.items():
                    value = " ".join([v.replace("\n", "") for v in value])
                    file.write("{}: {}\n".format(key.replace("\\n", ""), value))
            file.write("\n")
        if after_txt:
            file.write(after_txt)
        file.write("\n")


def txt_read(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()
    return {"file_content": file_content}


def only_txt_dump(file_path, txt):
    with open(file_path, "a", encoding="utf-8") as file:
        for word in txt.split("\n"):
            file.write(word)
            file.write("\n")
        file.write("\n")
