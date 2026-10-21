import { useEffect, useRef, useState } from 'react';

export interface PriceLevel {
  price: number;
  size: number;
}

export interface OrderBook {
  symbol: string;
  bids: PriceLevel[];
  asks: PriceLevel[];
  u: number;
  seq: number;
}

export interface Trade {
  symbol: string;
  trade_id: string;
  price: number;
  size: number;
  side: string;
  timestamp: number;
}

export const useMarketData = (url: string) => {
  const [orderBook, setOrderBook] = useState<OrderBook | null>(null);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    const connect = () => {
      ws.current = new WebSocket(url);

      ws.current.onopen = () => {
        setIsConnected(true);
        console.log('Connected to market data websocket');
      };

      ws.current.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          if (message.type === 'orderbook') {
            setOrderBook(message.data);
          } else if (message.type === 'trade') {
            setTrades((prevTrades) => {
              const newTrades = [message.data, ...prevTrades];
              // Keep only the last 50 trades
              return newTrades.slice(0, 50);
            });
          }
        } catch (error) {
          console.error('Error parsing websocket message:', error);
        }
      };

      ws.current.onclose = () => {
        setIsConnected(false);
        console.log('Websocket connection closed. Reconnecting...');
        setTimeout(connect, 3000);
      };

      ws.current.onerror = (error) => {
        console.error('Websocket error:', error);
        ws.current?.close();
      };
    };

    connect();

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [url]);

  return { orderBook, trades, isConnected };
};
