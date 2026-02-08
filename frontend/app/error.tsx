'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error('Application error:', error);
  }, [error]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md text-center">
        <div className="mx-auto bg-red-100 text-red-600 rounded-full w-16 h-16 flex items-center justify-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>

        <h2 className="text-2xl font-bold text-gray-800 mb-2">Something went wrong</h2>
        <p className="text-gray-600 mb-6">
          We encountered an error while processing your request. Please try again.
        </p>

        <div className="bg-red-50 text-red-700 rounded-lg p-4 text-left text-sm mb-6">
          <p className="font-medium">Error details:</p>
          <p>{error.message}</p>
          {error.digest && <p>Digest: {error.digest}</p>}
        </div>

        <button
          onClick={() => reset()}
          className="w-full py-3 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition"
        >
          Try Again
        </button>

        <p className="text-gray-500 text-sm mt-4">
          If the problem persists, please contact support.
        </p>
      </div>
    </div>
  );
}