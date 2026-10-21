"use client";

import React, { useState, useEffect } from 'react';
import OrderBookComponent from '@/components/OrderBook';
import TradesComponent from '@/components/Trades';
import { useMarketData } from '@/hooks/useMarketData';

export default function Home() {
  // Use environment variable or default to localhost
  const wsUrl = process.env.NEXT_PUBLIC_BACKEND_WS_URL || 'ws://localhost:8000/ws/market';
  const { orderBook, trades, isConnected } = useMarketData(wsUrl);

  const [mounted, setMounted] = useState(false);
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div className="min-h-screen bg-black text-gray-100 p-4 md:p-8">
      <header className="mb-8 flex justify-between items-end border-b border-gray-800 pb-4">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">SUPERSTORM AI</h1>
          <p className="text-gray-400 mt-1">Real-Time Crypto Intelligence Engine</p>
        </div>
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500 shadow-[0_0_8px_#22c55e]' : 'bg-red-500'}`}></div>
          <span className="text-sm font-medium text-gray-300">
            {isConnected ? 'Live Market Data Connected' : 'Disconnected / Reconnecting...'}
          </span>
        </div>
      </header>

      <main className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Order Book Panel */}
          <section className="flex flex-col gap-4">
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
              <OrderBookComponent orderBook={orderBook} />
            </div>
          </section>

          {/* Trade Tape Panel */}
          <section className="flex flex-col gap-4">
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
              <TradesComponent trades={trades} />
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
