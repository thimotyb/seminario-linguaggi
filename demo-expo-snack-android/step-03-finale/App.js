import React, { useState } from "react";
import {
  FlatList,
  Pressable,
  SafeAreaView,
  StatusBar,
  StyleSheet,
  Text,
  View,
} from "react-native";

const requirements = [
  { id: "build", label: "Build automatizzata", detail: "Artefatti riproducibili" },
  { id: "config", label: "Configurazione esterna", detail: "Niente segreti nel codice" },
  { id: "logs", label: "Log centralizzati", detail: "Diagnostica oltre la singola VM" },
  { id: "health", label: "Health check", detail: "Stato osservabile dall'orchestratore" },
  { id: "stateless", label: "Servizio stateless", detail: "Scaling orizzontale più semplice" },
];

export default function App() {
  const [selected, setSelected] = useState(new Set());
  const score = selected.size;
  const percentage = (score / requirements.length) * 100;
  const message =
    score === requirements.length
      ? "Ottima base per il cloud"
      : score >= 3
        ? "Buona base, restano alcuni gap"
        : "Prima consolidiamo le fondamenta";

  function toggleRequirement(id) {
    setSelected((current) => {
      const next = new Set(current);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }

  return (
    <SafeAreaView style={styles.screen}>
      <StatusBar barStyle="light-content" />
      <View style={styles.container}>
        <Text style={styles.eyebrow}>SEMINARIO · REACT NATIVE</Text>
        <Text style={styles.title}>Cloud Readiness Check</Text>
        <Text style={styles.subtitle}>Tocca i requisiti già soddisfatti.</Text>

        <View style={styles.summary}>
          <View style={styles.summaryRow}>
            <Text style={styles.message}>{message}</Text>
            <Text style={styles.score}>{score}/{requirements.length}</Text>
          </View>
          <View style={styles.track}>
            <View style={[styles.progress, { width: `${percentage}%` }]} />
          </View>
        </View>

        <FlatList
          data={requirements}
          keyExtractor={(item) => item.id}
          extraData={selected}
          contentContainerStyle={styles.list}
          renderItem={({ item }) => {
            const checked = selected.has(item.id);
            return (
              <Pressable
                onPress={() => toggleRequirement(item.id)}
                accessibilityRole="checkbox"
                accessibilityState={{ checked }}
                style={({ pressed }) => [
                  styles.card,
                  checked && styles.cardSelected,
                  pressed && styles.cardPressed,
                ]}
              >
                <Text style={styles.cardIcon}>{checked ? "✓" : "○"}</Text>
                <View style={styles.cardCopy}>
                  <Text style={styles.cardTitle}>{item.label}</Text>
                  <Text style={styles.cardDetail}>{item.detail}</Text>
                </View>
              </Pressable>
            );
          }}
        />

        <Pressable
          onPress={() => setSelected(new Set())}
          disabled={score === 0}
          style={[styles.reset, score === 0 && styles.resetDisabled]}
        >
          <Text style={styles.resetText}>Azzera checklist</Text>
        </Pressable>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: "#0f172a" },
  container: { flex: 1, paddingHorizontal: 22, paddingTop: 34, paddingBottom: 16 },
  eyebrow: { color: "#38bdf8", fontSize: 12, fontWeight: "800", letterSpacing: 1.2 },
  title: { color: "white", fontSize: 32, fontWeight: "800", marginTop: 8 },
  subtitle: { color: "#94a3b8", fontSize: 16, marginTop: 8 },
  summary: { backgroundColor: "#1e293b", borderRadius: 18, padding: 16, marginTop: 22 },
  summaryRow: { flexDirection: "row", alignItems: "center", justifyContent: "space-between", gap: 12 },
  message: { color: "#e2e8f0", flex: 1, fontWeight: "700" },
  score: { color: "#38bdf8", fontSize: 22, fontWeight: "900" },
  track: { height: 8, backgroundColor: "#334155", borderRadius: 999, marginTop: 14, overflow: "hidden" },
  progress: { height: "100%", backgroundColor: "#38bdf8", borderRadius: 999 },
  list: { paddingVertical: 18 },
  card: { flexDirection: "row", alignItems: "center", backgroundColor: "#1e293b", borderWidth: 1, borderColor: "#334155", borderRadius: 16, padding: 16, marginBottom: 10 },
  cardSelected: { backgroundColor: "#0c4a6e", borderColor: "#38bdf8" },
  cardPressed: { opacity: 0.75 },
  cardIcon: { color: "#38bdf8", fontSize: 25, width: 36 },
  cardCopy: { flex: 1 },
  cardTitle: { color: "#f8fafc", fontSize: 16, fontWeight: "700" },
  cardDetail: { color: "#94a3b8", fontSize: 13, marginTop: 3 },
  reset: { alignItems: "center", backgroundColor: "#38bdf8", borderRadius: 12, padding: 14 },
  resetDisabled: { opacity: 0.35 },
  resetText: { color: "#082f49", fontWeight: "900" },
});

