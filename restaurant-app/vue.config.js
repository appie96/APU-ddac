const { defineConfig } = require('@vue/cli-service')
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // Django 서버 주소
        changeOrigin: true,
        transpileDependencies: true
      },
    },
  },
};
