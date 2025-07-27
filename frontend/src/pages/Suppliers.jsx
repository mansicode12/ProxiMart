import React, { useEffect, useState } from "react";
import SupplierCard from "../components/SupplierCard";
import { getSuppliers } from "../utils/api";
import { useNavigate } from "react-router-dom"; // ✅ Add this

const Suppliers = () => {
  const [suppliers, setSuppliers] = useState([]);
  const navigate = useNavigate(); // ✅ hook to navigate

  useEffect(() => {
    const fetchSuppliers = async () => {
      try {
        const data = await getSuppliers();
        console.log("Fetched suppliers:", data);
        setSuppliers(data);
      } catch (error) {
        console.error("Failed to fetch suppliers:", error.message);
      }
    };

    fetchSuppliers();
  }, []);

  // ✅ Click handler: go to detail page
  const handleSupplierClick = (supplier) => {
    navigate(`/supplier/${supplier.id}`);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold text-yellow-600 mb-4">
        Available Suppliers
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {suppliers.length > 0 ? (
          suppliers.map((supplier, index) => (
            <SupplierCard
              key={index}
              supplier={supplier}
              onClick={handleSupplierClick}
            />
          ))
        ) : (
          <p className="text-gray-500">No suppliers found.</p>
        )}
      </div>
    </div>
  );
};

export default Suppliers;
