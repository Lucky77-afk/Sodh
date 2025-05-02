import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import logo from '../assets/logo.svg';

const Header = () => {
  const location = useLocation();
  
  // Navigation links with matching paths
  const navLinks = [
    { path: '/', name: 'Dashboard' },
    { path: '/transactions', name: 'Transactions' },
    { path: '/account', name: 'Account' },
    { path: '/smart-contract', name: 'Smart Contract' },
    { path: '/whitepaper', name: 'Whitepaper' },
    { path: '/tutorial', name: 'Tutorial' }
  ];

  return (
    <header className="bg-gray-800 shadow-md">
      <div className="container mx-auto px-4 py-3">
        <div className="flex justify-between items-center">
          {/* Logo and Title */}
          <div className="flex items-center">
            <img src={logo} alt="Sodh Logo" className="h-10 w-10 mr-3" />
            <h1 className="text-xl font-bold text-gradient">Sodh - Solana Blockchain Explorer</h1>
          </div>
          
          {/* Mobile menu button - for responsive design */}
          <div className="block lg:hidden">
            <button className="flex items-center px-3 py-2 border rounded text-green-400 border-green-400 hover:text-white hover:border-white">
              <svg className="fill-current h-3 w-3" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <title>Menu</title>
                <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z" />
              </svg>
            </button>
          </div>
          
          {/* Navigation Links - hidden on mobile */}
          <nav className="hidden lg:flex lg:items-center">
            <ul className="flex space-x-4">
              {navLinks.map((link) => (
                <li key={link.path}>
                  <Link 
                    to={link.path} 
                    className={`px-3 py-2 rounded-md ${
                      location.pathname === link.path 
                        ? 'bg-gradient-to-r from-green-400 to-purple-500 text-white' 
                        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                    }`}
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </div>
        
        {/* Mobile Navigation - shown on mobile */}
        <div className="lg:hidden hidden">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navLinks.map((link) => (
              <Link 
                key={link.path} 
                to={link.path} 
                className={`block px-3 py-2 rounded-md ${
                  location.pathname === link.path 
                    ? 'bg-gradient-to-r from-green-400 to-purple-500 text-white' 
                    : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                }`}
              >
                {link.name}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;