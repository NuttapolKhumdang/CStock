const express = require('express');
const router = express.Router();

const Product = require('../models/Product');

router.get("/", (req, res, next) => res.json({ Root: "CSTORE", Patch: "0.0.1" }));

module.exports = router;