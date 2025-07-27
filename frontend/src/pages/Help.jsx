import React, { useEffect, useState } from "react";
import { getFAQs } from "../utils/api"; 

const Help = () => {
  const [faqs, setFaqs] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchFAQs = async () => {
      try {
        const data = await getFAQs();
        setFaqs(data.faqs); 
      } catch (err) {
        setError("Failed to load FAQs");
      }
    };

    fetchFAQs();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold text-yellow-600 mb-4">FAQs</h1>

      {error && <p className="text-red-500">{error}</p>}

      <div className="grid grid-cols-1 gap-4">
        {faqs.length > 0 ? (
          faqs.map((faq, index) => (
            <div
              key={index}
              className="bg-white shadow-md p-4 rounded-xl border border-yellow-300"
            >
              <h3 className="font-semibold text-lg text-gray-800 mb-1">
                Q: {faq.question}
              </h3>
              <p className="text-gray-700">A: {faq.answer}</p>
            </div>
          ))
        ) : (
          <p className="text-gray-500">No FAQs found.</p>
        )}
      </div>
    </div>
  );
};

export default Help;
