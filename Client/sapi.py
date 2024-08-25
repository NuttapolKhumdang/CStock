import requests
ROOTURL = "http://localhost:3000/api/client"

def logres(res):
    print(res.status_code, "=>", res.json())

class API:
    def __init__(self, url):
        self.url = url
    
    def getProduct(self, _id = None):
        res = requests.get(f"{self.url}/id/{_id}" if _id else self.url)
        return res

    def addProduct(self, title, details, price, category, subcate, Quantity, MinStock, MaxStock):
        res = requests.post(self.url, json={
            "Title": title,
            "Details": details,
            "Price": price,

            "Category": category,
            "Subcate": subcate,

            "Quantity": Quantity,
            "MinStock": MinStock,
            "MaxStock": MaxStock,
        })

        # logres(res)
        return res

    def updateProduct(self, _id, title, details, price, category, subcate, Quantity, MinStock, MaxStock):
        res = requests.post(self.url + '/id/' + _id, json={
            "_id" : _id,
            "Title": title,
            "Details": details,

            # "Brand": brand,
            "Price": price,

            "Category": category,
            "Subcate": subcate,

            "Quantity": Quantity,
            "MinStock": MinStock,
            "MaxStock": MaxStock,
        })

        # logres(res)
        return res


    def newCategory(self, Title):
        res = requests.post(self.url + '/category', json={ "Title": Title })
        # logres(res)
        return res

    def getCategory(self, Id=None):
        res = requests.get(self.url + '/category', params = { "_id": Id })
        # logres(res)
        return res

    def updateCategory(self, Id, Title):
        res = requests.get(self.url + '/category/update', params = { "_id": Id, "Title": Title })
        # logres(res)
        return res

    def deleteDocument(self, module, _id):
        res = requests.delete(ROOTURL + '/' + module + '/' + _id)
        # logres(res)
        return res


if __name__ == '__main__':
    connect = API(ROOTURL)