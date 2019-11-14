const CompressionPlugin = require("compression-webpack-plugin")
const path = require('path')
//const debug = process.env.NODE_ENV != 'production'
const debug = false
module.exports = {
    publicPath: process.env.NODE_ENV === "production" ? "./" : "/",
    outputDir: "./dist",
    indexPath: "./dist/index.html",
    filenameHashing: false,
    productionSourceMap: false,
    devServer: {
        host: '0.0.0.0',
        port: 8080,
        https: false,
        hot: true
    },
    pluginOptions: {},
    configureWebpack: config=>{
        return {
            /**
            externals: {
                'vue': 'Vue',
                'element-ui': 'ELEMENT',
                'vue-router': 'VueRouter'
            },
            */
            plugins: [
                new CompressionPlugin({
                    //test:/\.js$|\.html$|.\css/, //匹配文件名
                    threshold: 10240, //超过10k的数据压缩
                    deleteOriginalAssets: false //不删除源文件
                })
            ]
        }
    },
}
