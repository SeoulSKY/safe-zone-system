import process from 'process';

export default ({config}) => {
  if (process.env.SAFEZONE_ENVIRONMENT === 'production') {
    if (!process.env.SAFEZONE_HOST) {
      throw new Error(
          'SAFEZONE_ENVIRONMENT = \'production\', ' +
          'missing SAFEZONE_HOST environment variable');
    }
    return {
      ...config,
      extra: {
        production: true,
        host: process.env.SAFEZONE_HOST,
      },
    };
  }
  return {
    ...config,
    extra: {
      host: process.env.SAFEZONE_HOST || undefined,
    },
  };
};

