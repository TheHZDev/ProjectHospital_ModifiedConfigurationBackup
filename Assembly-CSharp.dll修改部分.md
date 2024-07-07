## Assembly-CSharp.dll是什么？

Assembly-CSharp.dll 是Unity游戏《Project Hospital》的主要代码部分，由于它使用Mono作为运行后端，因此能轻松地被 [dnSpy](https://github.com/dnSpyEx/dnSpy) 进行反编译及修改。  

我已经修改了其中部分功能函数，以实现降低游戏难度的效果。    

## 修改一：角色编辑器

类名：`CharacterEditorController`

函数名：`RandomizeCharacter`

原始反编译代码：
```csharp
// Token: 0x06001E11 RID: 7697 RVA: 0x0014EB38 File Offset: 0x0014CF38
private void RandomizeCharacter(string gender = null)
{
	this.DeleteCharacter();
	this.SetCharacterLevel();
	GameDBDepartment departmentType = Hospital.Instance.GetActiveDepartment().GetDepartmentType();
	if (this.m_characterType == LopitalTypes.CharacterDoctor || this.m_characterType == LopitalTypes.CharacterDoctorWithInterns || this.m_characterType == LopitalTypes.CharacterSurgeon || this.m_characterType == LopitalTypes.CharacterAdvancedDiagnoses || this.m_characterType == LopitalTypes.CharacterAnesteziologist)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterDoctor(departmentType, null, Vector2i.ZERO_VECTOR, this.m_characterLevel, this.m_characterLevel, null, gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterNurse || this.m_characterType == LopitalTypes.CharacterSurgeryNurse || this.m_characterType == LopitalTypes.CharacterSpecialistNurse)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterNurse(null, Vector2i.ZERO_VECTOR, 1, 1, null, gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterReceptionist)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterNurse(null, Vector2i.ZERO_VECTOR, 2, 2, Database.Instance.GetEntry<GameDBSkill>("SKILL_NURSE_SPEC_RECEPTIONIST"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterLabSpecialist || this.m_characterType == LopitalTypes.CharacterTechnologist || this.m_characterType == LopitalTypes.CharacterAdvancedBiochemist)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterLabSpecialist(departmentType, null, Vector2i.ZERO_VECTOR, 1, 1, null, gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterUSGTechnologist)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterLabSpecialist(departmentType, null, Vector2i.ZERO_VECTOR, this.m_characterLevel, this.m_characterLevel, Database.Instance.GetEntry<GameDBSkill>("SKILL_LAB_SPECIALIST_SPEC_USG"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterCardiolog)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterLabSpecialist(departmentType, null, Vector2i.ZERO_VECTOR, this.m_characterLevel, this.m_characterLevel, Database.Instance.GetEntry<GameDBSkill>("SKILL_LAB_SPECIALIST_SPEC_CARDIOLOGY"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterNeurolog)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterLabSpecialist(departmentType, null, Vector2i.ZERO_VECTOR, this.m_characterLevel, this.m_characterLevel, Database.Instance.GetEntry<GameDBSkill>("SKILL_LAB_SPECIALIST_SPEC_NEUROLOGY"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterRadiolog)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterLabSpecialist(departmentType, null, Vector2i.ZERO_VECTOR, 2, 2, Database.Instance.GetEntry<GameDBSkill>("SKILL_LAB_SPECIALIST_SPEC_RADIOLOGY"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterJanitor)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterJanitor(null, Vector2i.ZERO_VECTOR, 1, 1, null, gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterPharmacologist)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterLabSpecialist(departmentType, null, Vector2i.ZERO_VECTOR, 2, 2, Database.Instance.GetEntry<GameDBSkill>("DLC_SKILL_LAB_SPECIALIST_SPEC_PHARMACOLOGY"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterVendorJanitor)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterJanitor(null, Vector2i.ZERO_VECTOR, 2, 2, Database.Instance.GetEntry<GameDBSkill>("DLC_SKILL_JANITOR_SPEC_VENDOR"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterManagerJanitor)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterJanitor(null, Vector2i.ZERO_VECTOR, 2, 2, Database.Instance.GetEntry<GameDBSkill>("DLC_SKILL_JANITOR_SPEC_MANAGER"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	this.CreatePerkSets(this.m_character);
	this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredLevel = this.m_character.GetComponent<EmployeeComponent>().m_state.m_level;
	this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredSalaryRandomization = global::UnityEngine.Random.Range(0f, 1f);
	this.m_character.GetComponent<EmployeeComponent>().m_state.m_employeeType = this.m_characterType;
	PortraitManager.Instance.CreatePortraitSlot(this.m_character);
	this.m_negativePerksCount = 0;
	this.m_positivePerksCount = 0;
	this.FillCharacterData();
}
```

修改后的反编译代码：
```csharp
// Token: 0x06001EE1 RID: 7905
private void RandomizeCharacter(string gender = null)
{
	this.DeleteCharacter();
	this.SetCharacterLevel();
	GameDBDepartment departmentType = Hospital.Instance.GetActiveDepartment().GetDepartmentType();
	if (this.m_characterType == LopitalTypes.CharacterDoctor || this.m_characterType == LopitalTypes.CharacterDoctorWithInterns || this.m_characterType == LopitalTypes.CharacterSurgeon || this.m_characterType == LopitalTypes.CharacterAdvancedDiagnoses || this.m_characterType == LopitalTypes.CharacterAnesteziologist)
	{
		if ((departmentType.DatabaseID.ToString() == "DPT_ICU" || departmentType.DatabaseID.ToString() == "DLC_DPT_PATHOLOGY") && this.m_characterType == LopitalTypes.CharacterDoctor)
		{
			this.m_character = LopitalEntityFactory.CreateCharacterDoctor(departmentType, null, Vector2i.ZERO_VECTOR, 2, 2, null, gender);
		}
		else
		{
			this.m_character = LopitalEntityFactory.CreateCharacterDoctor(departmentType, null, Vector2i.ZERO_VECTOR, 4, 4, null, gender);
		}
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterNurse || this.m_characterType == LopitalTypes.CharacterSurgeryNurse || this.m_characterType == LopitalTypes.CharacterSpecialistNurse)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterNurse(null, Vector2i.ZERO_VECTOR, 2, 2, null, gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterReceptionist)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterNurse(null, Vector2i.ZERO_VECTOR, 2, 2, Database.Instance.GetEntry<GameDBSkill>("SKILL_NURSE_SPEC_RECEPTIONIST"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterLabSpecialist || this.m_characterType == LopitalTypes.CharacterTechnologist || this.m_characterType == LopitalTypes.CharacterAdvancedBiochemist)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterLabSpecialist(departmentType, null, Vector2i.ZERO_VECTOR, 1, 1, null, gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterUSGTechnologist)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterLabSpecialist(departmentType, null, Vector2i.ZERO_VECTOR, this.m_characterLevel, this.m_characterLevel, Database.Instance.GetEntry<GameDBSkill>("SKILL_LAB_SPECIALIST_SPEC_USG"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterCardiolog)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterLabSpecialist(departmentType, null, Vector2i.ZERO_VECTOR, this.m_characterLevel, this.m_characterLevel, Database.Instance.GetEntry<GameDBSkill>("SKILL_LAB_SPECIALIST_SPEC_CARDIOLOGY"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterNeurolog)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterLabSpecialist(departmentType, null, Vector2i.ZERO_VECTOR, this.m_characterLevel, this.m_characterLevel, Database.Instance.GetEntry<GameDBSkill>("SKILL_LAB_SPECIALIST_SPEC_NEUROLOGY"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterRadiolog)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterLabSpecialist(departmentType, null, Vector2i.ZERO_VECTOR, 2, 2, Database.Instance.GetEntry<GameDBSkill>("SKILL_LAB_SPECIALIST_SPEC_RADIOLOGY"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterJanitor)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterJanitor(null, Vector2i.ZERO_VECTOR, 1, 1, null, gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterPharmacologist)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterLabSpecialist(departmentType, null, Vector2i.ZERO_VECTOR, 2, 2, Database.Instance.GetEntry<GameDBSkill>("DLC_SKILL_LAB_SPECIALIST_SPEC_PHARMACOLOGY"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterVendorJanitor)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterJanitor(null, Vector2i.ZERO_VECTOR, 2, 2, Database.Instance.GetEntry<GameDBSkill>("DLC_SKILL_JANITOR_SPEC_VENDOR"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	else if (this.m_characterType == LopitalTypes.CharacterManagerJanitor)
	{
		this.m_character = LopitalEntityFactory.CreateCharacterJanitor(null, Vector2i.ZERO_VECTOR, 2, 2, Database.Instance.GetEntry<GameDBSkill>("DLC_SKILL_JANITOR_SPEC_MANAGER"), gender);
		this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredForDepartment = departmentType;
	}
	this.CreatePerkSets(this.m_character);
	this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredLevel = this.m_character.GetComponent<EmployeeComponent>().m_state.m_level;
	this.m_character.GetComponent<EmployeeComponent>().m_state.m_hiredSalaryRandomization = global::UnityEngine.Random.Range(0f, 1f);
	this.m_character.GetComponent<EmployeeComponent>().m_state.m_employeeType = this.m_characterType;
	PortraitManager.Instance.CreatePortraitSlot(this.m_character);
	this.m_negativePerksCount = 0;
	this.m_positivePerksCount = 0;
	this.FillCharacterData();
}
```

效果：  
1、当创建非“ICU”及“病理学科室”的门诊医生和值班医生时，将默认其等级为第 4 级（可启用高级技能）而非默认的 2 级。  
2、根据第 1 点，现在“急诊科”门诊医生在角色编辑器的创建过程中，其角色等级从 1 级改为 4 级。  
3、创建所有科室的所有岗位的护士时，其默认等级为 2 级而不是 1 级。

## 修改二：接诊台分诊

命名空间：`Lopital`

类名：`ProcedureScriptExaminationReceptionFast`

函数名：`ResolveComplainedAboutHazardousSymptoms`

原始反编译代码：
```c#
// Token: 0x0600154B RID: 5451 RVA: 0x000E00F0 File Offset: 0x000DE4F0
public int ResolveComplainedAboutHazardousSymptoms()
{
    int num = 0;
    BehaviorPatient component = this.m_stateData.m_procedureScene.m_patient.GetEntity().GetComponent<BehaviorPatient>();
    for (int i = 0; i < component.m_state.m_medicalCondition.GetSpawnedSymptomCount(); i++)
    {
        Symptom symptom = component.m_state.m_medicalCondition.m_symptoms[i];
        if (symptom.m_hidden && symptom.m_symptom.Entry.Hazard >= BehaviorPatient.HAZARD_LEVEL_FOR_RECEPTION && symptom.m_patientKnowsAndComplains)
        {
            component.m_state.m_medicalCondition.m_symptoms[i].m_hidden = false;
            num++;
        }
    }
    return num;
}
```

修改后的反编译代码：
```csharp
// Token: 0x060015AE RID: 5550 RVA: 0x000E172C File Offset: 0x000DF92C
public int ResolveComplainedAboutHazardousSymptoms()
{
	int num = 0;
	BehaviorPatient component = this.m_stateData.m_procedureScene.m_patient.GetEntity().GetComponent<BehaviorPatient>();
	for (int i = 0; i < component.m_state.m_medicalCondition.GetSpawnedSymptomCount(); i++)
	{
		Symptom symptom = component.m_state.m_medicalCondition.m_symptoms[i];
		if (symptom.m_hidden && symptom.m_symptom.Entry.Hazard >= BehaviorPatient.HAZARD_LEVEL_FOR_RECEPTION && symptom.m_patientKnowsAndComplains)
		{
			component.m_state.m_medicalCondition.m_symptoms[i].m_hidden = false;
			num++;
		}
		else if (symptom.m_hidden && symptom.m_symptom.Entry.Hazard == SymptomHazard.Low && global::UnityEngine.Random.Range(0f, 1f) <= 0.8f)
		{
			component.m_state.m_medicalCondition.m_symptoms[i].m_hidden = false;
			num++;
		}
		else if (symptom.m_hidden && symptom.m_symptom.Entry.Hazard >= SymptomHazard.High && global::UnityEngine.Random.Range(0f, 1f) <= 0.1f)
		{
			component.m_state.m_medicalCondition.m_symptoms[i].m_hidden = false;
			num++;
		}
	}
	return num;
}
```

效果：  
1、原有的症状等级大于等于默认等级（中，Medium）且病人可以抱怨该症状后，该症状变为可见的 **原有逻辑** 不变。  
2、该症状的等级为低（Low）及以下时，有80%的概率直接暴露出来。  
3、该症状的等级为高（High）及以上时，有10%的概率直接暴露出来。

其他备注部分：  
1、病症的等级枚举：
```csharp
// Token: 0x0200012F RID: 303
public enum SymptomHazard
{
	// Token: 0x04000B03 RID: 2819
	Unknown,
	// Token: 0x04000B04 RID: 2820
	None,
	// Token: 0x04000B05 RID: 2821
	Low,
	// Token: 0x04000B06 RID: 2822
	Medium,
	// Token: 0x04000B07 RID: 2823
	High,
	// Token: 0x04000B08 RID: 2824
	Positive
}
```