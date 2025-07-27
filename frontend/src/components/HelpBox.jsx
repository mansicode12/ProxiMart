import React from "react";

const HelpBox = ({ question, answer }) => {
  return (
    <div className="bg-yellow-100 border-l-4 border-yellow-500 p-4 rounded-2xl shadow-sm mb-4">
      <h3 className="text-md font-semibold text-gray-800">{question}</h3>
      <p className="text-gray-700 mt-1">{answer}</p>
    </div>
  );
};

export default HelpBox;
