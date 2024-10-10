import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FileList = () => {
  const [files, setFiles] = useState([]);
  
  
  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/pdf-files`);
        const sortedFiles = response.data.sort((a, b) => {
          const timeA = new Date(a.createdAt).getTime();
          const timeB = new Date(b.createdAt).getTime();
          return timeA - timeB;
        });

        setFiles(sortedFiles);
      } catch (error) {
        console.error('Error fetching files:', error);
      }
    };

    fetchFiles();
  }, []);

  return (
    <div className="container mx-auto my-8 px-3">
      <h1 className="text-2xl font-bold mb-4">PDF Files</h1>
      <ul className="list-disc pl-4">
        {files.map((file, index) => (
          <li key={index} className="mb-2">
            <a
              href={`https://btp-dsd-server.vercel.app/${file}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              {file}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FileList;
