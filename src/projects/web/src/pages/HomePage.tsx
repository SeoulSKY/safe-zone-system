import React, {useEffect, useState} from 'react';
/**
import { MibsApi } from 'mibs';
const mibsApi = new MibsApi();
**/

/**
 * N/B:
 * Please change return type in jsdoc and method
 * declaration(line 11 and 13)
 * @method
 * @return {ReactElement}
 */
export default function HomePage() {
  const [cmsText, setCmsText] = useState('No Response');
  const [mibsText, setMibsText] = useState('No Response');

  useEffect(() => {
    fetch('http://localhost/cms/hello', {method: 'GET'})
        .then((response: Response) => {
          console.log('response', response);
          return response.text();
        })
        .then(setCmsText)
        .catch((error: Error) => setCmsText(`Error: ${error.message}`));

    fetch('http://localhost/mibs/hello', {method: 'GET'})
        .then((response: Response) => response.text() )
        .then(setMibsText)
        .catch((error: Error) => setMibsText(`Error: ${error.message}`));
  }, [setCmsText, setMibsText]);

  return (
    <div>
      <p>Home Page</p>
      <p>{`CMS Response: ${cmsText}`}</p>
      <p>{`MIBS Response: ${mibsText}`}</p>
    </div>
  );
}
