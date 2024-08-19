"use client";

import { useEffect, useState } from 'react';
import api from '@/utils/api';
import { API_POSTS } from '@/constants/routes';
import PoemModal from '@/app/components/PoemModal';
import Header from '@/app/components/Header';
import PoemCard from '@/app/components/PoemCard';

export interface PoemList {
  id: number;
  title: string;
  content: string;
  author_id: number;
};

const Feed = () => {
  const [poems, setPoems] = useState<PoemList[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [selectedPoem, setSelectedPoem] = useState<PoemList | null>(null);

  const fetchPoems = async (page: number) => {
    try {
      setLoading(true);
      const data = await api.get<any>(`${API_POSTS}?skip=${page-1}`);
      setPoems(data.poems);
      setTotalPages(data.total_pages);
    } catch (error) {
      setError('Error when loading poems');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPoems(page);
  }, [page]);

  const openModal = (poem: PoemList) => {
    setSelectedPoem(poem);
  };

  const closeModal = () => {
    setSelectedPoem(null);
  };

  const handlePreviousPage = () => {
    if (page > 1) {
      setPage(page - 1);
    }
  };

  const handleNextPage = () => {
    if (page < totalPages) {
      setPage(page + 1);
    }
  };

  if (loading && page === 1) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className=" h-screen bg-gray-100">
      <Header />
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 p-4">
        {poems.map(poem => <PoemCard poem={poem} onClick={() => openModal(poem)} />)}
      </div>

      <div className="flex justify-between items-center mt-10 p-4">
        <button
          onClick={handlePreviousPage}
          disabled={page === 1}
          className={`px-4 py-2 bg-blue-500 text-white rounded ${page === 1 ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          Left
        </button>

        <span className='text-black'>Page {page} / {totalPages}</span>

        <button
          onClick={handleNextPage}
          disabled={page === totalPages}
          className={`px-4 py-2 bg-blue-500 text-white rounded ${page === totalPages ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          Right
        </button>
      </div>

      {selectedPoem && (
        <PoemModal poem={selectedPoem} onClose={closeModal} />
      )}
    </div>
  );
};

export default Feed;
