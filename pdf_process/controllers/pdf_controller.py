import pdfplumber

print(pdfplumber.__version__)
from collections import defaultdict

class PDFController:
    def pdf_parsing_pages(self, pdf_file):
        preprocess_pdf = pdfplumber.open(pdf_file)
        preprocess_p = preprocess_pdf.pages
        return preprocess_pdf, preprocess_p

    def pdf_parsing_txt_and_table(self, page):
        preprocess_tables = page.extract_tables()
        preprocess_find_tables = page.find_tables()
        preprocess_info = page.extract_text_lines()
        return (
            preprocess_tables,
            preprocess_find_tables,
            preprocess_info,
        )

    def _pdf_table_convert(
        self,
        preprocess_table,
        label_count,
    ):
        for idx, table in enumerate(preprocess_table):
            for sub_idx, text in enumerate(table):
                if text == None and idx == 0:
                    table[sub_idx] = table[sub_idx - 1]
                elif text == None and idx > label_count:
                    table[sub_idx] = preprocess_table[idx - 1][sub_idx]
                elif idx > 0 and table[0] == None:
                    preprocess_table[idx][0] = preprocess_table[idx - 1][0]

    def pdf_search_label_location_count(self, preprocess_table):
        label_count = 0
        for label in preprocess_table[1:]:
            if label[0] == None:
                label_count += 1
            else:
                break
        self._pdf_table_convert(preprocess_table, label_count)
        return label_count

    def pdf_table_label_parsing(self, label_count, table_labels):
        label_list = []
        if label_count == 0:
            label_list = table_labels
        else:
            for label_idx, label in enumerate(table_labels[0]):
                for idx in range(label_count):
                    if idx == 0:
                        result_label = label
                    if (
                        result_label == table_labels[idx + 1][label_idx]
                        or None == table_labels[idx + 1][label_idx]
                    ):
                        pass
                    else:
                        result_label += ", " + table_labels[idx + 1][label_idx]
                label_list.append(result_label)
        return label_list

    def pdf_table_result_label_list(self, label_list):
        one_label_result_list = []
        non_label_result_list = []
        for values in label_list[1:]:
            tmp_dict = defaultdict(list)
            for k, v in zip(label_list[0], values):
                tmp_dict[k].append(v)
            one_label_result_list.append(tmp_dict)

        for texts in label_list:
            tmp_dict = {}
            tmp_dict[texts[0]] = texts[1:]
            non_label_result_list.append(tmp_dict)
        labels_keys = list(one_label_result_list[0].keys())
        if "," not in labels_keys[1]:
            return one_label_result_list
        return non_label_result_list

    def pdf_table_result_list(self, label_count, label_list, preprocess_table):
        result_list = []
        for values in preprocess_table[label_count + 1 :]:
            tmp_dict = defaultdict(list)
            for k, v in zip(label_list, values):
                if v == None:
                    continue
                tmp_dict[k].append(v)
            result_list.append(tmp_dict)
        return result_list

    def result_cleaning(self, result_dict):
        import os
        from .common_controller import json_dump, json_load
        from ..config.cfg import json_path

        json_dump(result_dict, json_path)
        cleaning_result_table_text_dict = json_load(json_path)

        tmp_list = []
        label_list = list(result_dict[0].keys())
        for idx, row in enumerate(result_dict):
            tmp_list.append(row)
            for label in label_list:
                if idx == 0:
                    break
                if len(tmp_list[0][label]) == len(row[label]):
                    for sub_idx, (previous_text, current_text) in enumerate(
                        zip(tmp_list[0][label], row[label])
                    ):
                        if sub_idx == 0:
                            continue
                        if previous_text == current_text:
                            if (
                                tmp_list[0][label][sub_idx - 1]
                                != row[label][sub_idx - 1]
                            ):
                                cleaning_result_table_text_dict[idx][label] = (
                                    result_dict[idx][label][:sub_idx]
                                )
                                break
                            elif (
                                tmp_list[0][label][sub_idx - 1]
                                == row[label][sub_idx - 1]
                            ):
                                if len(
                                    cleaning_result_table_text_dict[idx - 1][label]
                                ) != len(result_dict[idx - 1][label]):
                                    cleaning_result_table_text_dict[idx][
                                        label
                                    ] = result_dict[idx][label][
                                        : len(
                                            cleaning_result_table_text_dict[idx - 1][
                                                label
                                            ]
                                        )
                                    ]
                                    break
            if idx != 0:
                tmp_list = tmp_list[1:]

        if os.path.exists(json_path):
            os.remove(json_path)
        return cleaning_result_table_text_dict

    def total_pdf_parsing(
        self, result, page_table_list, page_info, table_bbox, idx, txt_path
    ):
        from .common_controller import txt_dump

        _, table_top, _, table_bottom = table_bbox
        text_add = []
        last_text_add = []
        for page_idx, data_info in enumerate(page_info):
            if table_top > data_info["top"]:
                text_add.append(f"{data_info['text']}\n")
            elif idx != len(page_table_list) - 1 and table_bottom < data_info["bottom"]:
                page_info = page_info[page_idx:]
                break
            if idx == len(page_table_list) - 1 and table_bottom < data_info["bottom"]:
                last_text_add.append(f"{data_info['text']}\n")
        if len(last_text_add) > 0:
            txt_dump(txt_path, " ".join(text_add), result, " ".join(last_text_add))
        else:
            txt_dump(txt_path, " ".join(text_add), result)
        return page_info