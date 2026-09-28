# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class DailyArxivPipeline:
    def process_item(self, item: dict, spider):
        item["pdf"] = item.get("pdf") or f"https://arxiv.org/pdf/{item['id']}"
        item["abs"] = item.get("abs") or f"https://arxiv.org/abs/{item['id']}"
        item["authors"] = item.get("authors", [])
        item["title"] = item.get("title", "")
        item["categories"] = item.get("categories", [])
        item["comment"] = item.get("comment")
        item["summary"] = item.get("summary", "")
        return item