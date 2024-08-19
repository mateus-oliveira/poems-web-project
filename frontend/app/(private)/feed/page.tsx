"use client";

import { useEffect, useState } from 'react';
import api from '@/utils/api';
import { API_POSTS } from '@/constants/routes';
import PoemModal from '@/app/components/PoemModal';
import Header from '@/app/components/Header';

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

  if (loading && page === 1) return <div>Carregando...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="p-4">
      <Header />
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        {poems.map(poem => (
          <div 
            key={poem.id} 
            onClick={() => openModal(poem)}
            className="cursor-pointer max-w-sm mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
            <div className="px-6 py-4">
              <h3 className="text-xl font-semibold text-gray-800 mb-2">{poem.title}</h3>
              <p className="text-gray-600 text-base">See more...</p>
            </div>
          </div>
        ))}
      </div>

      <div className="flex justify-between items-center mt-10">
        <button
          onClick={handlePreviousPage}
          disabled={page === 1}
          className={`px-4 py-2 bg-blue-500 text-white rounded ${page === 1 ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          Left
        </button>

        <span>Page {page} / {totalPages}</span>

        <button
          onClick={handleNextPage}
          disabled={page === totalPages}
          className={`px-4 py-2 bg-blue-500 text-white rounded ${page === totalPages ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          Right
        </button>
      </div>

      {loading && page > 1 && <div>Loading...</div>}

      {selectedPoem && (
        <PoemModal poem={selectedPoem} onClose={closeModal} />
      )}
    </div>
  );
};

export default Feed;
