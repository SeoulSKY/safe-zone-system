import React, { useEffect, useState } from 'react';

export default function GetRequest() {
  const [cmsText, setCmsText] = useState('No Response')
  const [mibsText, setMibsText] = useState('No Response')

  useEffect(() => {
    fetch('http://localhost/cms/hello', {method: 'GET'})
      .then((response: Response) => {console.log('response', response); return response.text()})
      .then(setCmsText)
      .catch((error: Error) => setCmsText(`Error: ${error.message}`))

    fetch('http://localhost/mibs/hello', {method: 'GET'})
      .then((response: Response) => response.text() )
      .then(setMibsText)
      .catch((error: Error) => setMibsText(`Error: ${error.message}`))
  }, [setCmsText, setMibsText])

  return (
    <div>
      <p>Home Screen</p>
      <p>{`CMS Response: ${cmsText}`}</p>
      <p>{`MIBS Response: ${mibsText}`}</p>
    </div>
  );
}
