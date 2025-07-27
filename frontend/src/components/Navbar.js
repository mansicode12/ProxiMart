import React from "react";
import { Link, useLocation } from "react-router-dom";

const Navbar = () => {
  const { pathname } = useLocation();

  const navItems = [
    { name: "Suppliers", path: "/suppliers" },
    { name: "Orders", path: "/orders" },
    { name: "Inventory", path: "/inventory" },
    { name: "Help", path: "/help" },
  ];

  return (
    <nav className="bg-yellow-400 shadow-md px-6 py-4 flex justify-between items-center">
      <h1 className="text-2xl font-bold text-gray-900">ProxiMart</h1>
      <div className="flex gap-6">
        {navItems.map((item) => (
          <Link
            key={item.name}
            to={item.path}
            className={`text-lg font-medium ${
              pathname === item.path
                ? "text-white underline underline-offset-4"
                : "text-gray-800 hover:text-white"
            }`}
          >
            {item.name}
          </Link>
        ))}
      </div>
    </nav>
  );
};

export default Navbar;
