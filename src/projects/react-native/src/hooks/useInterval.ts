import {assert} from '@/common/assertions';
import {useEffect, useRef} from 'react';

/**
 * Runs callback every
 * @param {Function} callback a function to be run.
 * @param {number} interval the interval to run the function at.
 */
export function useInterval(callback: () => void, interval: number) {
  assert(interval > 0, 'interval not > 0');
  const savedCallback = useRef();
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    const runCallback = () => savedCallback.current();
    if (interval !== null) {
      const id = setInterval(runCallback, interval);
      return () => {
        clearInterval(id);
      };
    }
  }, [callback, interval]);
}
