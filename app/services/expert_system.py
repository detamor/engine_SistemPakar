"""
Expert System Service untuk menghitung Certainty Factor
Menggunakan metode Certainty Factor (CF) untuk diagnosis penyakit tanaman hias
"""
from typing import List, Dict, Any
from loguru import logger
import numpy as np


class ExpertSystemService:
    """
    Service untuk melakukan perhitungan Certainty Factor
    dalam sistem pakar diagnosis penyakit tanaman hias
    """
    
    def calculate_certainty_factor(
        self,
        plant_id: int,
        symptoms: List[Dict[str, Any]],
        diseases_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Menghitung Certainty Factor untuk setiap kemungkinan penyakit
        
        Formula CF:
        CF(H,E) = CF(E) * CF(Rule)
        CF_combine = CF_old + (CF_new * (1 - CF_old))
        
        Args:
            plant_id: ID tanaman
            symptoms: List gejala yang dipilih user dengan CF user
            diseases_data: Data penyakit beserta gejala dan CF rule dari pakar
            
        Returns:
            Dict berisi hasil diagnosis dengan penyakit terpilih dan CF value
        """
        try:
            # Dictionary untuk menyimpan hasil CF per penyakit
            disease_cf_results = {}
            
            # Iterasi setiap penyakit
            for disease in diseases_data:
                disease_id = disease['id']
                disease_name = disease['name']
                disease_symptoms = disease.get('symptoms', [])
                
                # Inisialisasi CF untuk penyakit ini
                cf_combined = 0.0
                matched_symptoms = []
                
                # Iterasi gejala yang dipilih user
                for user_symptom in symptoms:
                    user_symptom_id = user_symptom['symptom_id']
                    user_cf = user_symptom['user_cf']
                    
                    # Cari gejala yang cocok di rule penyakit ini
                    for disease_symptom in disease_symptoms:
                        if disease_symptom['symptom_id'] == user_symptom_id:
                            # CF dari pakar (rule)
                            rule_cf = disease_symptom.get('certainty_factor', 0.0)
                            
                            # Hitung CF untuk gejala ini
                            # CF(H,E) = CF(E) * CF(Rule)
                            symptom_cf = user_cf * rule_cf
                            
                            matched_symptoms.append({
                                'symptom_id': user_symptom_id,
                                'user_cf': user_cf,
                                'rule_cf': rule_cf,
                                'symptom_cf': symptom_cf
                            })
                            
                            # Combine CF menggunakan formula:
                            # CF_combine = CF_old + (CF_new * (1 - CF_old))
                            if cf_combined == 0:
                                cf_combined = symptom_cf
                            else:
                                cf_combined = cf_combined + (symptom_cf * (1 - cf_combined))
                            
                            break
                
                # Simpan hasil untuk penyakit ini
                disease_cf_results[disease_id] = {
                    'disease_id': disease_id,
                    'disease_name': disease_name,
                    'certainty_value': round(cf_combined, 4),
                    'matched_symptoms': matched_symptoms,
                    'matched_count': len(matched_symptoms),
                    'solution': disease.get('solution', ''),
                    'prevention': disease.get('prevention', '')
                }
            
            # Urutkan berdasarkan CF value tertinggi
            sorted_diseases = sorted(
                disease_cf_results.values(),
                key=lambda x: x['certainty_value'],
                reverse=True
            )
            
            # Ambil penyakit dengan CF tertinggi
            top_disease = sorted_diseases[0] if sorted_diseases else None
            
            # Buat rekomendasi
            recommendation = self._generate_recommendation(top_disease, sorted_diseases)
            
            logger.info(f"Diagnosis selesai untuk plant_id {plant_id}")
            logger.info(f"Top disease: {top_disease['disease_name']} dengan CF: {top_disease['certainty_value']}")
            
            return {
                'disease_id': top_disease['disease_id'] if top_disease else None,
                'disease_name': top_disease['disease_name'] if top_disease else 'Tidak Diketahui',
                'certainty_value': top_disease['certainty_value'] if top_disease else 0.0,
                'recommendation': recommendation,
                'all_possibilities': sorted_diseases[:5]  # Top 5 kemungkinan
            }
            
        except Exception as e:
            logger.error(f"Error dalam perhitungan CF: {str(e)}")
            raise
    
    def _generate_recommendation(
        self,
        top_disease: Dict[str, Any],
        all_diseases: List[Dict[str, Any]]
    ) -> str:
        """
        Generate rekomendasi berdasarkan hasil diagnosis
        
        Args:
            top_disease: Penyakit dengan CF tertinggi
            all_diseases: Semua kemungkinan penyakit
            
        Returns:
            String rekomendasi
        """
        if not top_disease:
            return "Tidak dapat menentukan diagnosis. Silakan konsultasi dengan pakar."
        
        cf_value = top_disease['certainty_value']
        
        recommendation = f"Berdasarkan gejala yang Anda input, kemungkinan besar tanaman Anda terkena **{top_disease['disease_name']}** dengan tingkat kepastian {cf_value * 100:.2f}%.\n\n"
        
        if cf_value >= 0.7:
            recommendation += "**Tingkat Kepastian: TINGGI**\n"
            recommendation += "Diagnosis ini memiliki tingkat kepastian yang tinggi. Disarankan untuk segera melakukan penanganan.\n\n"
        elif cf_value >= 0.4:
            recommendation += "**Tingkat Kepastian: SEDANG**\n"
            recommendation += "Diagnosis ini memiliki tingkat kepastian sedang. Disarankan untuk melakukan observasi lebih lanjut atau konsultasi dengan pakar.\n\n"
        else:
            recommendation += "**Tingkat Kepastian: RENDAH**\n"
            recommendation += "Diagnosis ini memiliki tingkat kepastian rendah. Sangat disarankan untuk konsultasi langsung dengan pakar.\n\n"
        
        # Tambahkan solusi jika ada
        if top_disease.get('solution'):
            recommendation += f"**Solusi Penanganan:**\n{top_disease['solution']}\n\n"
        
        # Tambahkan pencegahan jika ada
        if top_disease.get('prevention'):
            recommendation += f"**Pencegahan:**\n{top_disease['prevention']}\n\n"
        
        # Jika ada kemungkinan lain
        if len(all_diseases) > 1:
            recommendation += f"\n**Kemungkinan Lain:**\n"
            for i, disease in enumerate(all_diseases[1:4], 1):  # Tampilkan 3 kemungkinan lain
                recommendation += f"{i}. {disease['disease_name']} (CF: {disease['certainty_value'] * 100:.2f}%)\n"
        
        return recommendation



