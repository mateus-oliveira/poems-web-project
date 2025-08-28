"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import swal from 'sweetalert';
import { API_LOGIN, FEED, REGISTER } from '@/constants/routes';
import api from '@/utils/api';
import { TOKEN, USER } from '@/constants/storage';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    await api.post(API_LOGIN, { email, password })
      .then((response: any) => {
        swal("Success!", "Welcome to Poems", "success");
        localStorage.setItem(TOKEN, response.access_token);
        localStorage.setItem(USER, JSON.stringify(response.user));
        router.push(FEED);
      })
      .catch(() => swal("Oops!", "Did you put the correct credentials?", "error"));
  };

  const handleRegisterRedirect = () => {
    router.push(REGISTER);
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <form
        onSubmit={handleLogin}
        className="flex flex-col items-center justify-between bg-white p-6 rounded shadow-md w-1/3 h-1/2">
        <h1 className="text-black text-2xl font-bold">Poems</h1>
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
        <button type="submit" className="bg-blue-500 text-white py-2 px-4 rounded w-full mb-4">
          Sign In
        </button>
        <button
          type="button"
          onClick={handleRegisterRedirect}
          className="bg-gray-500 text-white py-2 px-4 rounded w-full"
        >
          Sign Up
        </button>
      </form>
    </div>
  );
};

export default Login;
