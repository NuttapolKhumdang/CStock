const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const SchemaContent = new Schema({
    Title: String,
    Quantity: {
        type: Number,
        default: 0
    }
});

const mongooseModel = mongoose.model("Category", SchemaContent);
module.exports = mongooseModel;