const express = require('express');
const router = express.Router();

const Product = require('../models/Product');
const Category = require('../models/Category');

router.get("/", async (req, res, next) => res.json(await Product.find({})));
router.post("/", async (req, res, next) => {
    if (!req.body
        || !req.body.Title
        || !req.body.Price
        || !req.body.Category
    ) return res.status(401).json({ message: "Meta Content is Undefined" });

    const npdCategory = await Category.findOne({ Title: req.body.Category });
    await Category.findOneAndUpdate({ Title: req.body.Category }, { Quantity: npdCategory.Quantity++ });
    req.body["Category"] = npdCategory._id.toString();

    const newProduct = new Product(req.body);
    await newProduct.save();

    return res.json({ message: "OK", newProduct });
});

router.get("/id/:_id", async (req, res, next) => res.json(await Product.findById(req.params._id)));
router.post("/id/:_id", async (req, res, next) => {
    if (!req.body
        || !req.body._id
        || !req.body.Title
        || !req.body.Price
        || !req.body.Category
    ) return res.status(401).json({ message: "Meta Content is Undefined" });

    const opdProdcut = await Product.findById(req.params._id);
    const npdCategory = await Category.findOne({ Title: req.body.Category });

    if (opdProdcut.Category.toString() !== npdCategory._id.toString()){
        await Category.findByIdAndUpdate(opdProdcut.Category.toString(), { Quantity: npdCategory.Quantity-- });
        await Category.findByIdAndUpdate(npdCategory._id.toString(), { Quantity: npdCategory.Quantity++ });
    }

    req.body["Category"] = npdCategory._id.toString();

    const updated = await Product.findByIdAndUpdate(req.params._id, req.body);
    return res.json({ message: "OK", updated });
});

router.get("/category", async (req, res, next) => res.json(await Category.find(req.query._id ? { _id: req.query._id } : {})));
router.post("/category", async (req, res, next) => {
    const newCategory = new Category({ Title: req.body.Title });
    await newCategory.save();

    return res.json({ message: 'OK', newCategory });
});

router.get("/category/update", async (req, res, next) => {
    const updateCategory = await Category.findByIdAndUpdate(req.query._id, { Title: req.query.Title });
    return res.json({ message: 'OK', updateCategory });
});

router.delete('/:module/:id', async (req, res, next) => {
    let Document;
    if (req.params.module === "Category") Document = await Category.findByIdAndRemove(req.params.id);
    else if (req.params.module === "Product") Document = await Product.findByIdAndRemove(req.params.id);
    else return res.status(404).json({ message: "Document Not Found" });

    return res.json({ message: 'OK', Document, });
});

module.exports = router;