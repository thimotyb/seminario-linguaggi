import React, { useState } from "react";
import { Pressable, SafeAreaView, StyleSheet, Text, View } from "react-native";

const requirements = [
  { id: "build", label: "Build automatizzata" },
  { id: "config", label: "Configurazione esterna" },
  { id: "logs", label: "Log centralizzati" },
];

export default function App() {
  const [selected, setSelected] = useState(new Set());

  function toggleRequirement(id) {
    setSelected((current) => {
      const next = new Set(current);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }

  return (
    <SafeAreaView style={styles.screen}>
      <View style={styles.container}>
        <Text style={styles.eyebrow}>SEMINARIO · REACT NATIVE</Text>
        <Text style={styles.title}>Cloud Readiness Check</Text>
        <Text style={styles.subtitle}>Tocca i requisiti già soddisfatti.</Text>

        {requirements.map((item) => {
          const checked = selected.has(item.id);
          return (
            <Pressable
              key={item.id}
              onPress={() => toggleRequirement(item.id)}
              style={[styles.card, checked && styles.cardSelected]}
            >
              <Text style={styles.cardIcon}>{checked ? "✓" : "○"}</Text>
              <Text style={styles.cardText}>{item.label}</Text>
            </Pressable>
          );
        })}

        <Text style={styles.score}>{selected.size} di {requirements.length}</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: "#0f172a" },
  container: { flex: 1, padding: 24, paddingTop: 48 },
  eyebrow: { color: "#38bdf8", fontSize: 12, fontWeight: "800", letterSpacing: 1.2 },
  title: { color: "white", fontSize: 34, fontWeight: "800", marginTop: 10 },
  subtitle: { color: "#94a3b8", fontSize: 16, marginTop: 10, marginBottom: 24 },
  card: { flexDirection: "row", alignItems: "center", backgroundColor: "#1e293b", borderWidth: 1, borderColor: "#334155", borderRadius: 16, padding: 18, marginBottom: 12 },
  cardSelected: { backgroundColor: "#0c4a6e", borderColor: "#38bdf8" },
  cardIcon: { color: "#38bdf8", fontSize: 24, marginRight: 14 },
  cardText: { color: "#e2e8f0", fontSize: 16, fontWeight: "600" },
  score: { color: "white", fontSize: 22, fontWeight: "800", marginTop: 12 },
});

