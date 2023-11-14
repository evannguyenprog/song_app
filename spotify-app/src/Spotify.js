import React, { useState } from 'react';
import axios from 'axios';

const Spotify = () => {
  const [data, setData] = useState(null);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:3001/profile');
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div>
      <h1>Spotify Data</h1>
      <button onClick={fetchData}>Fetch Spotify Data</button>
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
};

export default Spotify;
