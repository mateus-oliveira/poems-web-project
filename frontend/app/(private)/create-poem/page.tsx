"use client";

import { useState } from 'react';
import api from '@/utils/api';
import swal from 'sweetalert';
import { API_POEMS, FEED } from '@/constants/routes';
import { useRouter } from 'next/navigation';


const CreatePoem = () => {
  const router = useRouter();
  const [title, setTitle] = useState<string>('');
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await api.post(API_POEMS, {title, content});
      swal("Success!", "Poem already created", "success");
      router.push(FEED);
    } catch (error) {
      setError('Error when trying create poem');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen w-full bg-gray-100">
      <form 
        onSubmit={handleSubmit}
        className="flex flex-col items-center justify-between bg-white p-6 rounded shadow-md w-1/3 h-1/2">
        <h1 className="text-black text-2xl font-bold mb-4">Create new poem</h1>
        <div className="mb-4 w-full">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="title">
            Title
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          />
        </div>

        <div className="mb-4 w-full">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="content">
            Content
          </label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          />
        </div>
        {error && <div className="text-red-500 mb-4">{error}</div>}
        <button
          type="submit"
          className={`bg-blue-500 text-white px-4 py-2 rounded ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
          disabled={loading}
        >
          {loading ? 'Creating...' : 'Create Poem'}
        </button>
      </form>
    </div>
  );
};

export default CreatePoem;
