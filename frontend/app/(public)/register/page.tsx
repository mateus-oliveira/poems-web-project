"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import swal from 'sweetalert';
import { API_REGISTER, LOGIN } from '@/constants/routes';
import api from '@/utils/api';

const Register = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const router = useRouter();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      swal("Ops!", "As senhas não coincidem!", "error");
      return;
    }

    await api.post(API_REGISTER, { name, email, password })
      .then(() => {
        swal("Success!", "Account creates!", "success");
        router.push(LOGIN);
      })
      .catch(() => swal("Oops!", "Error when trying create account", "error"));
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <form
        onSubmit={handleRegister}
        className="flex flex-col items-center justify-between bg-white p-6 rounded shadow-md w-1/3 h-2/3">
        <h1 className="text-black text-2xl font-bold">FeenixAI - Poem</h1>
        <div className="mb-4 w-full">
          <label className="block text-gray-700">Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="border rounded w-full py-2 px-3 text-gray-700"
            required
          />
        </div>
        <div className="mb-4 w-full">
          <label className="block text-gray-700">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="border rounded w-full py-2 px-3 text-gray-700"
            required
          />
        </div>
        <div className="mb-4 w-full">
          <label className="block text-gray-700">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="border rounded w-full py-2 px-3 text-gray-700"
            required
          />
        </div>
        <div className="mb-4 w-full">
          <label className="block text-gray-700">Confirm Password</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="border rounded w-full py-2 px-3 text-gray-700"
            required
          />
        </div>
        <button type="submit" className="bg-blue-500 text-white py-2 px-4 rounded w-full">
          Register
        </button>
      </form>
    </div>
  );
};

export default Register;
