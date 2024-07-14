from lxml import etree
import argparse, os.path
from concurrent.futures import ThreadPoolExecutor, Future, wait as waitThreads
from typing import List, Dict, Set, NamedTuple


class SymptomUnit(NamedTuple):
    databaseID: str
    filePath: str
    examinationIDs: Set[str]
    treatmentIDs: Set[str]


class DiagnoseUnit(NamedTuple):
    databaseID: str
    filePath: str
    symptomIDs: Set[str]
    examinationIDs: Set[str]
    treatmentIDs: Set[str]


class XMLFileData(NamedTuple):
    symptomUnits: List[SymptomUnit]
    diagnoseUnits: List[DiagnoseUnit]
    examinationIDs: Set[str]
    treatmentIDs: Set[str]


def __defaultXMLReader(filePath: str) -> XMLFileData:
    try:
        tData = etree.parse(filePath)
        return XMLFileData(
            __symptomsReader(tData, filePath) if __symptomsDetect(tData) else [],
            __diagnoseReader(tData, filePath) if __diagnoseDetect(tData) else [],
            __examinationReader(tData) if __examinationDetect(tData) else set(),
            __treatmentReader(tData) if __treatmentDetect(tData) else set()
        )
    except:
        return None


def __diagnoseDetect(fileData: etree._ElementTree) -> bool:
    return len(fileData.xpath('//GameDBMedicalCondition')) > 0


def __diagnoseReader(fileData: etree._ElementTree, filePath: str) -> List[DiagnoseUnit]:
    result = []
    for unit0 in fileData.xpath('//GameDBMedicalCondition'):
        # assert isinstance(unit0, etree._Element)
        databaseID = unit0.attrib['ID']
        symptomIDs = set([unit1.text for unit1 in unit0.xpath('.//GameDBSymptomRef')])
        examinationIDs = set([unit1.text for unit1 in unit0.xpath('.//ExaminationRef')])
        treatmentIDs = set([unit1.text for unit1 in unit0.xpath('.//TreatmentRef')])
        result.append(DiagnoseUnit(databaseID, filePath, symptomIDs, examinationIDs, treatmentIDs))
    return result


def __symptomsDetect(fileData: etree._ElementTree) -> bool:
    return len(fileData.xpath('//GameDBSymptom')) > 0


def __symptomsReader(fileData: etree._ElementTree, filePath: str) -> List[SymptomUnit]:
    result = []
    for unit0 in fileData.xpath('//GameDBSymptom'):
        assert isinstance(unit0, etree._Element)
        databaseID = unit0.attrib['ID']
        examinationIDs = set([unit1.text for unit1 in unit0.xpath('.//ExaminationRef')])
        treatmentIDs = set([unit1.text for unit1 in unit0.xpath('.//TreatmentRef')])
        result.append(SymptomUnit(databaseID, filePath, examinationIDs, treatmentIDs))
    return result


def __examinationDetect(fileData: etree._ElementTree) -> bool:
    return len(fileData.xpath('//GameDBExamination')) > 0


def __examinationReader(fileData: etree._ElementTree) -> Set[str]:
    resultSet = set()
    for unit0 in fileData.xpath('//GameDBExamination'):
        # assert isinstance(unit0, bs4Tag)
        resultSet.add(unit0.attrib['ID'])
    return resultSet


def __treatmentDetect(fileData: etree._ElementTree) -> bool:
    return len(fileData.xpath('//GameDBTreatment')) > 0


def __treatmentReader(fileData: etree._ElementTree) -> Set[str]:
    resultSet = set()
    for unit0 in fileData.xpath('//GameDBTreatment'):
        assert isinstance(unit0, etree._Element)
        resultSet.add(unit0.attrib['ID'])
    return resultSet

class LostData(NamedTuple):
    dataID: str
    filePath: str
    lostSymptomID: Set[str] | None
    lostExaminationID: Set[str]
    lostTreatmentID: Set[str]


def analyzeRelationshipLost(*toAnalyzeModFolder: str) -> List[LostData]:
    """
    评估所有症状和疾病的下属的症状/诊断方法/治疗方法的ID是否正确。

    :param toAnalyzeModFolder: 待分析的目录列数。
    :return: 缺失的ID数据
    """
    threadPools = ThreadPoolExecutor()
    threads: List[Future] = []

    for dataFolder in toAnalyzeModFolder:
        if os.path.isdir(dataFolder):
            for root, _, fileNames in os.walk(dataFolder, followlinks=True):
                for fileName in fileNames:
                    if fileName.endswith('.xml'):
                        threads.append(threadPools.submit(__defaultXMLReader, os.path.join(root, fileName)))
    print('正在等待所有读取任务完成，请稍等……')
    waitThreads(threads)

    diagnoseUnits: List[DiagnoseUnit] = []
    symptomUnits: List[SymptomUnit] = []
    symptoms: Set[str] = set()
    examinations: Set[str] = set()
    treatments: Set[str] = set()

    for taskUnit in threads:
        resultUnit = taskUnit.result()
        if resultUnit is not None and isinstance(resultUnit, XMLFileData):
            diagnoseUnits += resultUnit.diagnoseUnits
            symptomUnits += resultUnit.symptomUnits
            symptoms.update([unit1.databaseID for unit1 in resultUnit.symptomUnits])
            examinations.update(resultUnit.examinationIDs)
            treatments.update(resultUnit.treatmentIDs)

    result = []
    for diagnose in diagnoseUnits:
        tVar0 = diagnose.symptomIDs - symptoms
        tVar1 = diagnose.examinationIDs - examinations
        tVar2 = diagnose.treatmentIDs - treatments
        if len(tVar0) + len(tVar1) + len(tVar2) > 0:
            result.append(LostData(diagnose.databaseID, diagnose.filePath, tVar0, tVar1, tVar2))
    for symptom in symptomUnits:
        tVar1 = symptom.examinationIDs - examinations
        tVar2 = symptom.treatmentIDs - treatments
        if len(tVar1) + len(tVar2) > 0:
            result.append(LostData(symptom.databaseID, symptom.filePath, None, tVar1, tVar2))
    return result


if __name__ == '__main__':
    mainArgs = argparse.ArgumentParser(description='本程序用于审计疾病下属的症状/诊断方法/治疗方法的关联ID，以及症状下属的诊断/治疗方法的关联ID是否有误。', epilog='你可能需要在存在空格的路径两端使用英文双引号将其包裹。')
    mainArgs.add_argument('DataFolder', help='指定要审计的模组的目录，或者其依赖模组的目录（建议同时指定游戏的数据目录，多个路径之间使用空格分隔）。', nargs='+')
    workArgs = mainArgs.parse_args()
    if workArgs is not None:
        t1 = analyzeRelationshipLost(*workArgs.DataFolder)
        if len(t1) > 0:
            for t2 in t1:
                if t2.lostSymptomID is None:
                    print(f'检测到症状 {t2.dataID}（路径：{t2.filePath}） 存在的异常情况：')
                    if len(t2.lostExaminationID) > 0:
                        print('不存在的诊断方式ID：' + '、'.join(t2.lostExaminationID))
                    if len(t2.lostTreatmentID) > 0:
                        print('不存在的治疗方法ID：' + '、'.join(t2.lostTreatmentID))
                else:
                    print(f'检测到疾病 {t2.dataID}（路径：{t2.filePath}） 存在的异常情况：')
                    if len(t2.lostSymptomID) > 0:
                        print('不存在的症状ID：' + '、'.join(t2.lostSymptomID))
                    if len(t2.lostExaminationID) > 0:
                        print('不存在的诊断方式ID：' + '、'.join(t2.lostExaminationID))
                    if len(t2.lostTreatmentID) > 0:
                        print('不存在的治疗方法ID：' + '、'.join(t2.lostTreatmentID))
        else:
            print('检查完成！未发现问题！')
