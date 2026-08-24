import { useState, useEffect, useCallback } from 'react';
import { Navbar } from './components/Navbar';
import { VoiceHero } from './components/VoiceHero';
import { PipelineViewer } from './components/PipelineViewer';
import { ShoppingList } from './components/ShoppingList';
import { RecommendationSection } from './components/RecommendationSection';
import { SeasonalPicks } from './components/SeasonalPicks';
import { ProductSearch } from './components/ProductSearch';
import { AIInsightsPanel } from './components/AIInsightsPanel';
import { CommandHistory } from './components/CommandHistory';
import { ShoppingMode } from './components/ShoppingMode';

import { useSpeechRecognition } from './hooks/useSpeechRecognition';
import { useTextToSpeech } from './hooks/useTextToSpeech';
import { api } from './services/api';
import type {
  ShoppingItem,
  Product,
  RecommendationItem,
  SeasonalItem,
  SubstituteItem,
  InsightSummary,
  HistoryItem,
  PipelineInspection,
  LanguageMode
} from './types';

export function App() {
  const [language, setLanguage] = useState<LanguageMode>('en');
  const [shoppingList, setShoppingList] = useState<ShoppingItem[]>([]);
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([]);
  const [seasonalPicks, setSeasonalPicks] = useState<SeasonalItem[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [searchResults, setSearchResults] = useState<Product[] | null>(null);
  const [insights, setInsights] = useState<InsightSummary | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [pipeline, setPipeline] = useState<PipelineInspection | null>(null);

  const [isShoppingMode, setIsShoppingMode] = useState<boolean>(false);
  const [showPipeline, setShowPipeline] = useState<boolean>(true);
  const [lastMessage, setLastMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const { isMuted, toggleMute, speak } = useTextToSpeech(false);

  const refreshState = useCallback(async () => {
    try {
      const [listData, recsData, seasonData, prodsData, insightsData, histData] = await Promise.all([
        api.getShoppingList(),
        api.getRecommendations(),
        api.getSeasonalPicks(),
        api.getProducts(),
        api.getInsights(),
        api.getHistory(),
      ]);

      setShoppingList(listData);
      setRecommendations(recsData);
      setSeasonalPicks(seasonData);
      setProducts(prodsData);
      setInsights(insightsData);
      setHistory(histData.commands);
    } catch (err) {
      console.error('Failed to load initial data from server:', err);
    }
  }, []);

  useEffect(() => {
    refreshState();
  }, [refreshState]);

  const handleExecuteCommand = useCallback(async (text: string) => {
    if (!text.trim()) return;
    setIsLoading(true);
    setLastMessage(null);

    try {
      const res = await api.sendCommand(text, language);
      setPipeline(res.pipeline);
      setLastMessage(res.message);

      if (res.tts_message) {
        speak(res.tts_message, language);
      }

      if (res.intent === 'SEARCH_PRODUCT' && res.search_results) {
        setSearchResults(res.search_results);
      }

      await refreshState();
    } catch (err: any) {
      console.error('Command failed:', err);
      const errMsg = err.message || "Sorry, I couldn't understand that. Try saying 'Add 2 apples'.";
      setLastMessage(errMsg);
      speak(errMsg, language);
    } finally {
      setIsLoading(false);
    }
  }, [language, speak, refreshState]);

  const {
    voiceState,
    setVoiceState,
    interimTranscript,
    permissionError,
    startListening,
    stopListening,
  } = useSpeechRecognition({
    language,
    onResult: (transcript) => {
      handleExecuteCommand(transcript);
      setVoiceState('SUCCESS');
      setTimeout(() => setVoiceState('IDLE'), 2000);
    },
    onError: (err) => {
      setLastMessage(err);
    }
  });

  const handleTogglePurchased = async (id: number, currentStatus: boolean) => {
    try {
      setShoppingList(prev =>
        prev.map(i => (i.id === id ? { ...i, is_purchased: !currentStatus } : i))
      );
      await api.updateShoppingItem(id, { is_purchased: !currentStatus });
      await refreshState();
    } catch (err) {
      console.error('Failed to update status:', err);
      await refreshState();
    }
  };

  const handleUpdateQuantity = async (id: number, newQty: number) => {
    try {
      setShoppingList(prev =>
        prev.map(i => (i.id === id ? { ...i, quantity: newQty } : i))
      );
      await api.updateShoppingItem(id, { quantity: newQty });
      await refreshState();
    } catch (err) {
      console.error('Failed to update quantity:', err);
      await refreshState();
    }
  };

  const handleDeleteItem = async (id: number) => {
    try {
      setShoppingList(prev => prev.filter(i => i.id !== id));
      await api.deleteShoppingItem(id);
      await refreshState();
    } catch (err) {
      console.error('Failed to delete item:', err);
      await refreshState();
    }
  };

  const handleClearAll = async () => {
    try {
      setShoppingList([]);
      await api.clearShoppingList();
      await refreshState();
    } catch (err) {
      console.error('Failed to clear list:', err);
    }
  };

  const handleClearPurchased = async () => {
    try {
      setShoppingList(prev => prev.filter(i => !i.is_purchased));
      await api.clearPurchasedItems();
      await refreshState();
    } catch (err) {
      console.error('Failed to clear purchased items:', err);
    }
  };

  const handleUndo = async () => {
    try {
      const res = await api.undoLastAction();
      setLastMessage(res.message);
      speak(res.message, language);
      await refreshState();
    } catch (err) {
      console.error('Failed to undo:', err);
    }
  };

  const handleManualAdd = async (name: string, quantity: number, unit: string) => {
    try {
      await api.addShoppingItem({ name, quantity, unit });
      setLastMessage(`Added ${quantity} ${unit} of ${name}`);
      speak(`Added ${name}`, language);
      await refreshState();
    } catch (err) {
      console.error('Failed to add manual item:', err);
    }
  };

  const handleAddRecommendation = async (rec: RecommendationItem) => {
    try {
      await api.addShoppingItem({
        name: rec.product_name,
        brand: rec.preferred_brand,
        quantity: rec.preferred_quantity,
        unit: rec.preferred_unit,
        category: rec.category,
        estimated_price: rec.estimated_price,
      });
      setLastMessage(`Added ${rec.product_name} from your recommendations.`);
      speak(`Added ${rec.product_name}`, language);
      await refreshState();
    } catch (err) {
      console.error('Failed to add recommendation:', err);
    }
  };

  const handleDismissRecommendation = (productName: string) => {
    setRecommendations(prev => prev.filter(r => r.product_name !== productName));
  };

  const handleAddSeasonal = async (item: SeasonalItem) => {
    try {
      await api.addShoppingItem({
        name: item.name,
        quantity: 1,
        unit: item.unit,
        category: item.category,
        estimated_price: item.price,
      });
      setLastMessage(`Added seasonal pick: ${item.name}`);
      speak(`Added ${item.name}`, language);
      await refreshState();
    } catch (err) {
      console.error('Failed to add seasonal item:', err);
    }
  };

  const handleSearchProducts = async (query: string, minPrice?: number, maxPrice?: number) => {
    try {
      const results = await api.searchProducts(query, minPrice, maxPrice);
      setSearchResults(results);
    } catch (err) {
      console.error('Failed to search products:', err);
    }
  };

  const handleAddToCart = async (product: Product) => {
    try {
      await api.addShoppingItem({
        name: product.name,
        brand: product.brand,
        quantity: 1,
        unit: product.unit,
        category: product.category,
        estimated_price: product.price,
      });
      setLastMessage(`Added ${product.name} to list.`);
      speak(`Added ${product.name}`, language);
      await refreshState();
    } catch (err) {
      console.error('Failed to add catalog product:', err);
    }
  };

  const handleSelectSubstitute = async (sub: SubstituteItem) => {
    try {
      await api.addShoppingItem({
        name: sub.substitute_name,
        brand: sub.substitute_brand,
        quantity: 1,
        unit: 'piece',
        category: sub.category,
        estimated_price: sub.substitute_price,
      });
      setLastMessage(`Added alternative: ${sub.substitute_name} (₹${sub.substitute_price})`);
      speak(`Added alternative ${sub.substitute_name}`, language);
      await refreshState();
    } catch (err) {
      console.error('Failed to add substitute:', err);
    }
  };

  const handleCompleteTrip = async () => {
    try {
      await api.checkoutPurchased();
      setIsShoppingMode(false);
      setLastMessage('🎉 Shopping trip completed! Purchases logged to history.');
      speak('Shopping trip completed! Purchases logged to your history.', language);
      await refreshState();
    } catch (err) {
      console.error('Failed to complete trip:', err);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 pb-16">
      {/* Top Navbar */}
      <Navbar
        language={language}
        onLanguageChange={setLanguage}
        isMuted={isMuted}
        onToggleMute={toggleMute}
        isShoppingMode={isShoppingMode}
        onToggleShoppingMode={() => setIsShoppingMode(prev => !prev)}
        showPipeline={showPipeline}
        onTogglePipeline={() => setShowPipeline(prev => !prev)}
      />

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 space-y-8">
        {/* Voice Hero Centerpiece */}
        <VoiceHero
          voiceState={voiceState}
          interimTranscript={interimTranscript}
          onStartListening={startListening}
          onStopListening={stopListening}
          onSubmitText={handleExecuteCommand}
          permissionError={permissionError}
          lastMessage={lastMessage}
          language={language}
        />

        {/* NLU Pipeline Telemetry Viewer */}
        {showPipeline && (
          <PipelineViewer
            pipeline={pipeline}
            onClose={() => setShowPipeline(false)}
          />
        )}

        {/* Today's Categorized Shopping List */}
        <ShoppingList
          items={shoppingList}
          onTogglePurchased={handleTogglePurchased}
          onUpdateQuantity={handleUpdateQuantity}
          onDelete={handleDeleteItem}
          onClearAll={handleClearAll}
          onClearPurchased={handleClearPurchased}
          onUndo={handleUndo}
          onManualAdd={handleManualAdd}
        />

        {/* Smart Restock Recommendations (MAJOR DIFFERENTIATOR) */}
        <RecommendationSection
          recommendations={recommendations}
          onAdd={handleAddRecommendation}
          onDismiss={handleDismissRecommendation}
          onRefresh={refreshState}
          isLoading={isLoading}
        />

        {/* Seasonal Picks Bar */}
        <SeasonalPicks
          items={seasonalPicks}
          onAddSeasonal={handleAddSeasonal}
        />

        {/* Voice & Catalog Product Search */}
        <ProductSearch
          products={products}
          searchResults={searchResults}
          onSearch={handleSearchProducts}
          onAddToCart={handleAddToCart}
          onSelectSubstitute={handleSelectSubstitute}
        />

        {/* AI Insights & Shopping Pattern Breakdown */}
        <AIInsightsPanel insights={insights} />

        {/* Voice Activity & Command History */}
        <CommandHistory
          history={history}
          onUndo={handleUndo}
        />
      </main>

      {/* Shopping Session Mode (Focused In-Store UI) */}
      {isShoppingMode && (
        <ShoppingMode
          items={shoppingList}
          voiceState={voiceState}
          interimTranscript={interimTranscript}
          onStartListening={startListening}
          onStopListening={stopListening}
          onTogglePurchased={handleTogglePurchased}
          onCompleteTrip={handleCompleteTrip}
          onExitShoppingMode={() => setIsShoppingMode(false)}
        />
      )}
    </div>
  );
}

export default App;
