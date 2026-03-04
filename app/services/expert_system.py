"""
Expert System Service menggunakan Experta Library
Menggunakan metode Forward Chaining + Certainty Factor (CF) untuk diagnosis penyakit tanaman hias

Sistem Pakar Berbasis Web untuk Diagnosis Penyakit dan Modul Optimalisasi
Pemeliharaan Tanaman Hias di Parongpong

Forward Chaining:
- Mulai dari fakta (gejala yang dipilih user)
- Match dengan rules (aturan penyakit dengan gejala)
- Infer kesimpulan (penyakit yang mungkin)
- Hitung CF untuk setiap kesimpulan

Certainty Factor (CF):
Formula perhitungan CF sesuai dengan dokumen proyek:

1. Perhitungan CF Gejala:
   CF(H,E) = CF(E) * CF(Rule)
   Dimana:
   - CF(E) = CF dari user (user_cf) dengan nilai 0.0 - 1.0
   - CF(Rule) = CF dari pakar (rule_cf) dengan nilai 0.0 - 1.0
   
   Contoh: CFGejala = 0.6 * 0.6 = 0.36

2. Kombinasi CF untuk Multiple Gejala:
   CF_combine = CF_old + (CF_new * (1 - CF_old))
   
   Contoh perhitungan (dari dokumen proyek):
   - Gejala 1: CFGejala1 = 0.6 * 0.6 = 0.36
   - Gejala 2: CFGejala2 = 0.8 * 0.8 = 0.64
   - CFcombine1 = 0.36 + 0.64 * (1 - 0.36) = 0.7696
   - Gejala 3: CFGejala3 = 0.6 * 0.8 = 0.48
   - CFcombine2 = 0.7696 + 0.48 * (1 - 0.7696) = 0.880192
   - Gejala 4: CFGejala4 = 0.6 * 0.6 = 0.36
   - CFcombine3 = 0.880192 + 0.36 * (1 - 0.880192) = 0.92332288
   
   Persentase Keyakinan = CF_penyakit * 100
   Contoh: 0.92332288 * 100 = 92.332288%

3. Bobot Nilai CF User (dari dokumen):
   - Tidak Yakin: 0
   - Sedikit Yakin: 0.4
   - Cukup Yakin: 0.6
   - Yakin: 0.8
   - Sangat Yakin: 1.0

Implementasi menggunakan Experta Library untuk:
- Rule-based reasoning dengan Forward Chaining
- Pattern matching antara gejala user dengan aturan penyakit
- Automatic inference engine untuk menghasilkan kesimpulan
"""
from typing import List, Dict, Any, Optional
from loguru import logger

# Python 3.10+ compatibility fix for frozendict 1.2 (required by experta)
# collections.Mapping was moved to collections.abc.Mapping in Python 3.3
# and removed in Python 3.10+
import collections
import collections.abc
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    collections.Sequence = collections.abc.Sequence

from experta import Fact, KnowledgeEngine, Rule, Field, AS, MATCH


# Define Facts untuk Experta
class UserSymptom(Fact):
    """Fakta gejala yang dipilih user"""
    symptom_id = Field(int, mandatory=True)
    user_cf = Field(float, mandatory=True)  # CF dari user (0.0 - 1.0)


class DiseaseRule(Fact):
    """Fakta aturan penyakit dengan gejala"""
    disease_id = Field(int, mandatory=True)
    disease_name = Field(str, mandatory=True)
    symptom_id = Field(int, mandatory=True)
    rule_cf = Field(float, mandatory=True)  # CF dari pakar (0.0 - 1.0)
    solution = Field(str, default="")
    prevention = Field(str, default="")




class ExpertSystemEngine(KnowledgeEngine):
    """
    Knowledge Engine untuk sistem pakar menggunakan Experta
    Mengimplementasikan Forward Chaining:
    1. Mulai dari fakta (UserSymptom)
    2. Match dengan rules (DiseaseRule)
    3. Infer kesimpulan (penyakit dengan CF)
    """
    
    def __init__(self):
        super().__init__()
        self.disease_results = {}  # Menyimpan hasil CF per penyakit
    
    @Rule(
        AS.user_symptom << UserSymptom(
            symptom_id=MATCH.symptom_id,
            user_cf=MATCH.user_cf
        ),
        AS.disease_rule << DiseaseRule(
            disease_id=MATCH.disease_id,
            disease_name=MATCH.disease_name,
            symptom_id=MATCH.symptom_id,
            rule_cf=MATCH.rule_cf,
            solution=MATCH.solution,
            prevention=MATCH.prevention
        )
    )
    def calculate_symptom_cf(self, user_symptom, disease_rule, symptom_id, user_cf, disease_id, disease_name, rule_cf, solution, prevention):
        """
        Forward Chaining Rule: Match gejala dengan aturan penyakit
        Menghitung CF gejala: CF(H,E) = CF(E) * CF(Rule)
        
        Ini adalah Forward Chaining karena:
        - Mulai dari fakta (UserSymptom)
        - Mencari rules yang match (DiseaseRule dengan symptom_id yang sama)
        - Menginfer kesimpulan (penyakit dengan CF value)
        
        Contoh perhitungan sesuai dokumen proyek:
        - CFGejala1 = CF(user) * CF(pakar) = 0.6 * 0.6 = 0.36
        - CFGejala2 = CF(user) * CF(pakar) = 0.8 * 0.8 = 0.64
        - CFcombine1 = CFgejala1 + CFgejala2 * (1 - CFgejala1) = 0.36 + 0.64 * (1 - 0.36) = 0.7696
        - CFcombine2 = CFold1 + CFgejala3 * (1 - CFold1) = 0.7696 + 0.48 * (1 - 0.7696) = 0.880192
        """
        # Validasi CF values (harus dalam range 0.0 - 1.0)
        user_cf = max(0.0, min(1.0, float(user_cf)))
        rule_cf = max(0.0, min(1.0, float(rule_cf)))
        
        # Langkah 1: Hitung CF untuk gejala ini
        # Formula: CF(H,E) = CF(E) * CF(Rule)
        # Dimana: CF(E) = user_cf (CF dari user), CF(Rule) = rule_cf (CF dari pakar)
        # Contoh: CFGejala = 0.6 * 0.6 = 0.36
        symptom_cf = user_cf * rule_cf
        
        # Logging detail untuk debugging
        logger.debug(
            f"Gejala {symptom_id} match dengan penyakit {disease_name} (ID: {disease_id}): "
            f"CF_user={user_cf:.4f}, CF_pakar={rule_cf:.4f}, CF_gejala={symptom_cf:.4f}"
        )
        
        # Inisialisasi jika belum ada
        if disease_id not in self.disease_results:
            self.disease_results[disease_id] = {
                'disease_id': disease_id,
                'disease_name': disease_name,
                'cf_combined': 0.0,
                'matched_symptoms': [],
                'solution': solution or '',
                'prevention': prevention or ''
            }
        
        # Cek apakah gejala ini sudah pernah diproses untuk penyakit ini
        # (Handling gejala duplikat - ambil CF yang lebih tinggi)
        existing_symptom = None
        for idx, matched in enumerate(self.disease_results[disease_id]['matched_symptoms']):
            if matched['symptom_id'] == symptom_id:
                existing_symptom = idx
                break
        
        if existing_symptom is not None:
            # Gejala duplikat: gunakan CF yang lebih tinggi
            old_symptom_cf = self.disease_results[disease_id]['matched_symptoms'][existing_symptom]['symptom_cf']
            if symptom_cf > old_symptom_cf:
                logger.debug(f"Gejala {symptom_id} duplikat untuk penyakit {disease_id}, menggunakan CF yang lebih tinggi: {symptom_cf:.4f} > {old_symptom_cf:.4f}")
                # Update gejala dengan CF yang lebih tinggi
                self.disease_results[disease_id]['matched_symptoms'][existing_symptom] = {
                    'symptom_id': symptom_id,
                    'user_cf': user_cf,
                    'rule_cf': rule_cf,
                    'symptom_cf': symptom_cf
                }
                # Recalculate CF combined dari awal untuk konsistensi
                matched_symptoms = self.disease_results[disease_id]['matched_symptoms']
                if len(matched_symptoms) > 0:
                    cf_combined = matched_symptoms[0]['symptom_cf']
                    for matched in matched_symptoms[1:]:
                        cf_combined = cf_combined + (matched['symptom_cf'] * (1 - cf_combined))
                    self.disease_results[disease_id]['cf_combined'] = min(1.0, cf_combined)  # Clamp ke 1.0
            return  # Skip perhitungan lebih lanjut karena sudah di-handle
        
        # Tambahkan gejala yang cocok (gejala baru)
        self.disease_results[disease_id]['matched_symptoms'].append({
            'symptom_id': symptom_id,
            'user_cf': user_cf,
            'rule_cf': rule_cf,
            'symptom_cf': symptom_cf
        })
        
        # Langkah 2: Combine CF untuk multiple gejala
        # Formula: CF_combine = CF_old + (CF_new * (1 - CF_old))
        # Jika ini gejala pertama (CF_old = 0), langsung gunakan CF gejala
        # Jika sudah ada gejala sebelumnya, gunakan formula kombinasi
        # Contoh:
        #   - Gejala 1: CF_combined = 0.36 (langsung dari symptom_cf)
        #   - Gejala 2: CF_combined = 0.36 + (0.64 * (1 - 0.36)) = 0.7696
        #   - Gejala 3: CF_combined = 0.7696 + (0.48 * (1 - 0.7696)) = 0.880192
        current_cf = self.disease_results[disease_id]['cf_combined']
        if current_cf == 0:
            # Gejala pertama: langsung gunakan CF gejala
            self.disease_results[disease_id]['cf_combined'] = symptom_cf
            logger.debug(f"Gejala pertama untuk penyakit {disease_id}: CF_combined = {symptom_cf:.4f}")
        else:
            # Gejala berikutnya: kombinasi dengan CF yang sudah ada
            # CF_combine = CF_old + (CF_new * (1 - CF_old))
            new_cf = current_cf + (symptom_cf * (1 - current_cf))
            # Clamp ke maksimum 1.0 (untuk memastikan tidak melebihi 1.0 karena floating point error)
            self.disease_results[disease_id]['cf_combined'] = min(1.0, new_cf)
            logger.debug(
                f"Kombinasi CF untuk penyakit {disease_id}: "
                f"CF_old={current_cf:.4f}, CF_new={symptom_cf:.4f}, CF_combined={self.disease_results[disease_id]['cf_combined']:.4f}"
            )
    


class ExpertSystemService:
    """
    Service untuk melakukan perhitungan Certainty Factor
    menggunakan Experta library untuk rule-based reasoning
    """
    
    def calculate_certainty_factor(
        self,
        plant_id: int,
        symptoms: List[Dict[str, Any]],
        diseases_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Menghitung Certainty Factor menggunakan Forward Chaining + Experta
        
        Metode: Forward Chaining
        - Mulai dari fakta (gejala yang dipilih user)
        - Match dengan rules (aturan penyakit dengan gejala)
        - Infer kesimpulan (penyakit yang mungkin)
        - Hitung CF untuk setiap kesimpulan
        
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
            # Validasi input
            if not isinstance(diseases_data, list):
                logger.error(f"diseases_data harus list, tapi mendapat: {type(diseases_data)}")
                raise ValueError(f"diseases_data harus list, tapi mendapat: {type(diseases_data)}")
            
            if not isinstance(symptoms, list):
                logger.error(f"symptoms harus list, tapi mendapat: {type(symptoms)}")
                raise ValueError(f"symptoms harus list, tapi mendapat: {type(symptoms)}")
            
            # Inisialisasi Experta Knowledge Engine
            engine = ExpertSystemEngine()
            engine.reset()  # Reset engine untuk sesi baru
            
            # Reset hasil
            engine.disease_results = {}
            
            # 1. Declare Disease Rules sebagai Facts
            for disease in diseases_data:
                # Validasi bahwa disease adalah dict
                if not isinstance(disease, dict):
                    logger.warning(f"disease harus dict, mendapat: {type(disease)}, value: {disease}")
                    continue
                
                disease_id = disease.get('id')
                disease_name = disease.get('name', 'Unknown')
                disease_symptoms = disease.get('symptoms', [])
                solution = disease.get('solution', '')
                prevention = disease.get('prevention', '')
                
                # Validasi disease_symptoms adalah list
                if not isinstance(disease_symptoms, list):
                    logger.warning(f"disease_symptoms harus list untuk disease {disease_id}, mendapat: {type(disease_symptoms)}")
                    disease_symptoms = []
                
                # Declare setiap symptom rule sebagai fact
                for disease_symptom in disease_symptoms:
                    if not isinstance(disease_symptom, dict):
                        logger.warning(f"disease_symptom harus dict, mendapat: {type(disease_symptom)}")
                        continue
                    
                    symptom_id = disease_symptom.get('symptom_id') or disease_symptom.get('id')
                    rule_cf = float(disease_symptom.get('certainty_factor', 0.0) or disease_symptom.get('cf', 0.0))
                    
                    if symptom_id is None:
                        continue
                    
                    # Validasi CF value dari pakar (0.0 - 1.0)
                    rule_cf = max(0.0, min(1.0, rule_cf))
                    
                    # Declare DiseaseRule fact
                    engine.declare(
                        DiseaseRule(
                            disease_id=disease_id,
                            disease_name=disease_name,
                            symptom_id=symptom_id,
                            rule_cf=rule_cf,
                            solution=solution or '',
                            prevention=prevention or ''
                        )
                    )
            
            # 2. Declare User Symptoms sebagai Facts
            # Sort gejala berdasarkan symptom_id untuk konsistensi perhitungan
            sorted_symptoms = sorted(symptoms, key=lambda x: x.get('symptom_id', 0) if isinstance(x, dict) else 0)
            
            # Filter dan validasi gejala duplikat (ambil yang terakhir dengan CF tertinggi)
            unique_symptoms = {}
            for user_symptom in sorted_symptoms:
                if not isinstance(user_symptom, dict):
                    logger.warning(f"user_symptom harus dict, mendapat: {type(user_symptom)}")
                    continue
                
                symptom_id = user_symptom.get('symptom_id')
                user_cf = float(user_symptom.get('user_cf', 0.0))
                
                if symptom_id is None:
                    continue
                
                # Validasi CF value (0.0 - 1.0)
                user_cf = max(0.0, min(1.0, user_cf))
                
                # Handle gejala duplikat: simpan yang dengan CF tertinggi
                if symptom_id in unique_symptoms:
                    if user_cf > unique_symptoms[symptom_id]['user_cf']:
                        logger.debug(f"Gejala {symptom_id} duplikat, menggunakan CF yang lebih tinggi: {user_cf:.4f}")
                        unique_symptoms[symptom_id] = {'symptom_id': symptom_id, 'user_cf': user_cf}
                else:
                    unique_symptoms[symptom_id] = {'symptom_id': symptom_id, 'user_cf': user_cf}
            
            # Declare UserSymptom facts (hanya gejala unik)
            for symptom_data in unique_symptoms.values():
                engine.declare(
                    UserSymptom(
                        symptom_id=symptom_data['symptom_id'],
                        user_cf=symptom_data['user_cf']
                    )
                )
            
            logger.info(f"Memproses {len(unique_symptoms)} gejala unik dari {len(symptoms)} gejala input")
            
            # 3. Run Knowledge Engine (Forward Chaining)
            logger.info(f"Running Forward Chaining dengan Experta untuk {len(symptoms)} gejala dan {len(diseases_data)} penyakit")
            logger.info("Forward Chaining: Mulai dari fakta (gejala) → Match rules → Infer kesimpulan (penyakit)")
            engine.run()
            
            # 4. Ambil hasil dari engine
            disease_cf_results = engine.disease_results
            
            # 5. Proses hasil jika tidak ada yang match (engine mungkin tidak trigger rules)
            if not disease_cf_results:
                logger.warning("Tidak ada penyakit yang match dengan gejala yang dipilih")
                return {
                    'disease_id': None,
                    'disease_name': 'Tidak Diketahui',
                    'certainty_value': 0.0,
                    'recommendation': 'Tidak dapat menentukan diagnosis. Silakan pilih gejala lain atau konsultasi dengan pakar.',
                    'all_possibilities': []
                }
            
            # 6. Format hasil per penyakit
            formatted_results = []
            for disease_id, result in disease_cf_results.items():
                # Pastikan CF value dalam range 0.0 - 1.0
                cf_value = max(0.0, min(1.0, result['cf_combined']))
                
                formatted_results.append({
                    'disease_id': result['disease_id'],
                    'disease_name': result['disease_name'],
                    'certainty_value': round(cf_value, 4),
                    'matched_symptoms': result['matched_symptoms'],
                    'matched_count': len(result['matched_symptoms']),
                    'solution': result.get('solution', ''),
                    'prevention': result.get('prevention', '')
                })
                
                # Logging detail hasil per penyakit
                logger.info(
                    f"Penyakit {result['disease_name']} (ID: {disease_id}): "
                    f"CF={cf_value:.4f} ({cf_value*100:.2f}%), "
                    f"Matched {len(result['matched_symptoms'])} gejala"
                )
            
            # 7. Urutkan berdasarkan CF value tertinggi
            sorted_diseases = sorted(
                formatted_results,
                key=lambda x: x['certainty_value'],
                reverse=True
            )
            
            # 8. Ambil penyakit dengan CF tertinggi
            top_disease = sorted_diseases[0] if sorted_diseases else None
            
            # 9. Buat rekomendasi
            recommendation = self._generate_recommendation(top_disease, sorted_diseases)
            
            logger.info(f"Diagnosis selesai untuk plant_id {plant_id}")
            logger.info(f"Top disease: {top_disease['disease_name']} dengan CF: {top_disease['certainty_value']}")
            logger.info(f"Total {len(sorted_diseases)} kemungkinan penyakit ditemukan")
            
            return {
                'disease_id': top_disease['disease_id'] if top_disease else None,
                'disease_name': top_disease['disease_name'] if top_disease else 'Tidak Diketahui',
                'certainty_value': top_disease['certainty_value'] if top_disease else 0.0,
                'recommendation': recommendation,
                'all_possibilities': sorted_diseases[:5]  # Top 5 kemungkinan
            }
            
        except Exception as e:
            logger.error(f"Error dalam perhitungan CF dengan Experta: {str(e)}")
            logger.exception(e)
            raise
    
    def _generate_recommendation(
        self,
        top_disease: Optional[Dict[str, Any]],
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
