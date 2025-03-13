import js from "@eslint/js";
import { defineConfig } from "eslint/config";

export default defineConfig([
    {
        plugins: {
            js
        },
        extends: ["js/recommended"],
        rules: {
            "no-unused-vars": "warn"
            curly: ['warn', 'all'],
            '@typescript-eslint/no-unused-vars': ['warn', { args: 'none' }],
            eqeqeq: 'error',
            'no-empty-function': 'off',
        }
    }
]);
