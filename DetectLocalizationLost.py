import argparse
from lxml import etree
from typing import List, Dict, Set, NamedTuple, Any
import os.path
from concurrent.futures import ThreadPoolExecutor, Future, wait as waitThreads


class XMLFileData(NamedTuple):
    filePath: str  # 文件路径
    translationID: Set[str]  # 已存在的翻译ID数据
    normalIDs: Set[str]  # 非翻译的ID


def __defaultXMLReader(filePath: str, languageCode: str, onlyTranslation: bool = False) -> XMLFileData:
    """
    读取XML文件并返回数据。

    :param filePath: XML文件路径。
    :param languageCode: 仅限翻译文件读取时使用，匹配语言代码。
    :param onlyTranslation: 仅扫描翻译文件，用在原版游戏目录扫描中。
    """
    try:
        tData = etree.parse(filePath)
        translationSet = set()
        if __localizationDetect(tData, languageCode):
            translationSet = __localizationReader(tData, languageCode)
        resultSet = set()
        if not onlyTranslation:
            if __diagnoseDetect(tData):
                resultSet.update(__diagnoseReader(tData))
            if __symptomsDetect(tData):
                resultSet.update(__symptomsReader(tData))
            if __examinationDetect(tData):
                resultSet.update(__examinationReader(tData))
            if __treatmentDetect(tData):
                resultSet.update(__treatmentReader(tData))
        return XMLFileData(filePath, translationSet, resultSet)
    except:
        return None


def __localizationDetect(fileData: etree._ElementTree, languageCode: str) -> bool:
    for unit0 in fileData.xpath('//GameDBStringTable'):
        assert isinstance(unit0, etree._Element)
        if unit0.find('LanguageCode').text == languageCode:
            return True
    return False


def __localizationReader(fileData: etree._ElementTree, languageCode: str) -> Set[str]:
    resultSet = set()
    for unit0 in fileData.xpath('//GameDBStringTable'):
        # assert isinstance(unit0, bs4Tag)
        if unit0.find('LanguageCode').text == languageCode:
            for unit1 in unit0.xpath('.//LocID'):
                resultSet.add(unit1.text)
    return resultSet


def __diagnoseDetect(fileData: etree._ElementTree) -> bool:
    return len(fileData.xpath('//GameDBMedicalCondition')) > 0


def __diagnoseReader(fileData: etree._ElementTree) -> Set[str]:
    resultSet = set()
    for unit0 in fileData.xpath('//GameDBMedicalCondition'):
        # assert isinstance(unit0, bs4Tag)
        resultSet.add(unit0.attrib['ID'])
        resultSet.add(unit0.find('AbbreviationLocID').text)
    return resultSet


def __symptomsDetect(fileData: etree._ElementTree) -> bool:
    return len(fileData.xpath('//GameDBSymptom')) > 0


def __symptomsReader(fileData: etree._ElementTree) -> Set[str]:
    resultSet = set()
    for unit0 in fileData.xpath('//GameDBSymptom'):
        # assert isinstance(unit0, bs4Tag)
        resultSet.add(unit0.attrib['ID'])
        resultSet.add(unit0.find('DescriptionLocID').text)
    return resultSet


def __examinationDetect(fileData: etree._ElementTree) -> bool:
    return len(fileData.xpath('//GameDBExamination')) > 0


def __examinationReader(fileData: etree._ElementTree) -> Set[str]:
    resultSet = set()
    for unit0 in fileData.xpath('//GameDBExamination'):
        # assert isinstance(unit0, bs4Tag)
        resultSet.add(unit0.attrib['ID'])
        resultSet.add(unit0.find('AbbreviationLocID').text)
    return resultSet


def __treatmentDetect(fileData: etree._ElementTree) -> bool:
    return len(fileData.xpath('//GameDBTreatment')) > 0


def __treatmentReader(fileData: etree._ElementTree) -> Set[str]:
    resultSet = set()
    for unit0 in fileData.xpath('//GameDBTreatment'):
        assert isinstance(unit0, etree._Element)
        resultSet.add(unit0.attrib['ID'])
        resultSet.add(unit0.find('AbbreviationLocID').text)
    return resultSet


def analyzeLocalizationLost(toAnalyzeModFolder: List[str] | str, vanillaGameFolder: str,
                            languageCode: str = 'zh-Hans') -> Dict[str, str]:
    """
    读取所有翻译文件以确定是否存在翻译内容缺失的情况。

    :param toAnalyzeModFolder: 待分析的mod的数据目录，会读取所有的文件并解析。
    :param vanillaGameFolder: 原版游戏文件，只处理翻译文件。
    :param languageCode: 语言代码，默认设定为 zh-Hans，即简体中文。
    :return: Dict{缺损的词条ID -> 文件路径}
    """
    threadPool = ThreadPoolExecutor()
    threads: List[Future] = []
    if isinstance(toAnalyzeModFolder, str):
        toAnalyzeModFolder = [toAnalyzeModFolder]

    for root, _, fileNames in os.walk(vanillaGameFolder, followlinks=True):
        for fileName in fileNames:
            if fileName.endswith('.xml'):
                threads.append(threadPool.submit(__defaultXMLReader, os.path.join(root, fileName), languageCode, True))
    for folderPath in toAnalyzeModFolder:
        if os.path.isdir(folderPath):
            for root, _, fileNames in os.walk(folderPath, followlinks=True):
                for fileName in fileNames:
                    if fileName.endswith('.xml'):
                        threads.append(
                            threadPool.submit(__defaultXMLReader, os.path.join(root, fileName), languageCode, False))
    # 读取文件完成后自动分析
    print('正在等待所有读取任务完成……')
    waitThreads(threads)
    translationIDs = set()
    normalIDs = set()
    fileDigests: Dict[str, Set[str]] = {}
    for threadUnit in threads:
        resultUnit = threadUnit.result()
        # assert isinstance(resultUnit, XMLFileData)
        if resultUnit is None:
            continue
        translationIDs.update(resultUnit.translationID)
        normalIDs.update(resultUnit.normalIDs)
        if len(resultUnit.normalIDs) > 0:
            fileDigests[resultUnit.filePath] = normalIDs
    # 直接分析
    lostIDs = normalIDs - translationIDs
    if len(lostIDs) > 0:
        resultData = {}
        for lostID in lostIDs:
            for filePath in fileDigests:
                if lostID in fileDigests[filePath]:
                    resultData[lostID] = filePath
                    break
        return resultData
    else:
        return {}

if __name__ == '__main__':
    mainArgs = argparse.ArgumentParser(description='本程序用作翻译ID的缺失审计。被审计的范围包括：疾病名称及其描述，诊断方法的名称及其描述，疾病症状的名称及其描述，治疗方法的名称及其描述。', epilog='你可能需要在存在空格的路径两端使用英文双引号将其包裹。')
    mainArgs.add_argument('-g', '--game-folder', help='指定游戏《Project Hospital》的数据目录（StreamingAssets）的所在路径。')
    mainArgs.add_argument('-m', '--mod-folder', help='指定要审计的模组的目录，你可以通过多次指定该参数来审计多个模组，或添加依赖模组。', required=True, action='append')
    mainArgs.add_argument('-l', '--language-mode', help='指定审计时使用的翻译语言，默认使用 zh-Hans，即简体中文。', default='zh-Hans', choices=['en', 'cz', 'da', 'de', 'es', 'la', 'fr', 'hu', 'it', 'ja', 'kr', 'nl', 'ptbr', 'pl', 'ru', 'swe', 'tr', 'uk', 'zh-Hans', 'zhtw'])
    workArgs = mainArgs.parse_args()
    if workArgs is not None:
        t1 = analyzeLocalizationLost(workArgs.mod_folder, workArgs.game_folder, workArgs.language_mode)
        if len(t1) > 0:
            for t2 in t1:
                print(f'发现缺失的翻译ID {t2}，它可能来自于 {t1[t2]}。')
        else:
            print('检查结束！没有发现问题！')