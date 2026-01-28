import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import Index from "./pages/Index";
import Predict from "./pages/Predict";
import About from "./pages/About";
import NotFound from "./pages/NotFound";
import Molecular from "./pages/Molecular";
import Imaging from "./pages/Imaging";

const queryClient = new QueryClient();

const AnimatedRoutes = () => {
  const location = useLocation();

  return (
    <div key={location.pathname} className="animate-in fade-in-0 duration-300">
      <Routes location={location}>
        <Route path="/" element={<Index />} />
        <Route path="/synthetic" element={<Predict />} />
        <Route path="/molecular" element={<Molecular />} />
        <Route path="/imaging" element={<Imaging />} />

        {/* Backwards compatibility */}
        <Route path="/predict" element={<Navigate to="/synthetic" replace />} />

        <Route path="/about" element={<About />} />
        {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  );
};

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <AnimatedRoutes />
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
