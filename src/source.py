class Source:
    def __init__(self, filename, title = None, date = None, author = None, description = None, publisher = None, pages = None):
        self.filename = filename
        self.title = title
        self.date = date
        self.author = author
        self.description = description
        self.publisher = publisher
        self.pages = pages if pages is not None else []
