module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        targets: {
          chrome: 100,
        },
      },
    ],
    '@babel/preset-react',
    '@babel/preset-typescript',
  ],
  plugins: [
    // Devs tend to write `import { someIcon } from '@patternfly/react-icons';`
    // This transforms the import to be specific which prevents having to parse 2k+ icons
    // Also prevents potential bundle size blowups with CJS
    [
      'transform-imports',
      {
        '@patternfly/react-icons': {
          transform: (importName) =>
            `@patternfly/react-icons/dist/js/icons/${
              importName === 'PathMissingIcon'
                ? 'pathMissing-icon'
                : importName
                    .split(/(?=[A-Z])/)
                    .join('-')
                    .toLowerCase()
            }`,
          preventFullImport: true,
        },
      },
    ],
  ],
};
