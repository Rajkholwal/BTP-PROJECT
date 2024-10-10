import React from 'react';

const SvgDisplay = ({ svgContent }) => {
  return (
    <div
      dangerouslySetInnerHTML={{ __html: svgContent }}
    />
  );
};

export default SvgDisplay;
