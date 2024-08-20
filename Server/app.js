const http = require('http');
const express = require('express');
const cookieParser = require('cookie-parser');
const logger = require('morgan');

require('./modules/database');
const app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

const indexRouter = require('./routers/index');
const productRouter = require('./routers/product');
app.use('/', indexRouter);
app.use('/api/client', productRouter);

const port = process.env.PORT || '3000';
app.set('port', port);

const server = http.createServer(app);
server.listen(port);