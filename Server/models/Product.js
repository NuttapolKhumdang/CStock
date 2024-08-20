const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const SchemaContent = new Schema({
    Title: String,
    Details: String,

    Price: Number,

    Category: String,
    Subcate: String,

    Circulation: Array,
    Quantity: {
        type: Number,
        default: 0
    },

    MinStock: {
        type: Number,
        default: 0
    },
    MaxStock: {
        type: Number,
        default: 0
    },
});

const mongooseModel = mongoose.model("Product", SchemaContent);
module.exports = mongooseModel;