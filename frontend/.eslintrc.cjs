module.exports = {
  root: true,
  env: { browser: true, es2021: true },
  extends: [
    'plugin:vue/vue3-essential',
    'plugin:@typescript-eslint/recommended',
    'prettier'
  ],
  parserOptions: { ecmaVersion: 'latest', sourceType: 'module' },
  rules: {}
}

