let isEnabled = false;


export const enableAssertions = (enable: boolean): void => {
  console.log('Assertions enabled: ', enable);
  isEnabled = enable;
};


export const assert = (assertion: boolean, ...args: string[]): void => {
  if (isEnabled && !assertion) {
    console.assert(false, ...args);
    throw new Error('Assertion failed' +
      (args?.length > 0 ? ': ' + args.join(' ') : ''));
  }
};

