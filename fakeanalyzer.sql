-- phpMyAdmin SQL Dump
-- version 4.2.11
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: 09-Abr-2022 às 00:08
-- Versão do servidor: 5.6.21
-- PHP Version: 5.6.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `fakeanalyzer`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `mensagem`
--

CREATE TABLE IF NOT EXISTS `mensagem` (
  `md5` varchar(35) NOT NULL,
  `tipo` int(11) NOT NULL,
  `conteudo` varchar(500) NOT NULL,
  `verificado` int(11) NOT NULL,
  `fake` int(11) NOT NULL,
  `justificativa` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `mensagem`
--

INSERT INTO `mensagem` (`md5`, `tipo`, `conteudo`, `verificado`, `fake`, `justificativa`) VALUES
('02100545b6cd8fea6c825041ce29f12f', 3, 'https://noticias.uol.com.br/politica/ultimas-noticias/2020/07/07/jair-bolsonaro-testa-positivo-para-covid-19.htm', 1, 0, 'Se trata de uma notícia publicada pela equipe de notícias da UOL, e o conteúdo é de responsabilidade desta.'),
('027938f27db65f6ff4301c0fc12b9af9', 3, 'https://go.hurb.com/foto-de-morcego-do-tamanho-de-um-humano-viraliza-e-nao-e-fake/', 1, 0, 'essa espécie é nativa das Filipinas.'),
('066e4485ec84bf8ff974842350df1163', 2, '', 1, 1, 'Estas notícias nunca foram publicadas pelo jornal A Folha de São Paulo'),
('127ecf79a05bf8ca07136a0606bb28b1', 2, '', 1, 1, 'Matéria nunca foi publicada pelo jornal A Folha de São Paulo'),
('376ba093d2e53aa4f3744193712318f7', 1, 'ATENÇÃO!!!\nEsta noite, entre 18h00 e as 23h00, um satélite infravermelho da NASA medirá a temperatura corporal de toda a população, para mapear a taxa de contaminação do Covid-19.\nÉ muito importante que você esteja todo nú do lado de fora da sua casa, na varanda ou em frente a porta, enquanto segura seu RG na mão direita.\nÉ obrigatória a participação.', 1, 1, 'Isto é uma piada!'),
('37e404c5ecfad845ee7010be254b272f', 2, '', 1, 1, 'É uma piada, tenha bom humor!'),
('56dd314e169266acf63741aaf021a998', 3, 'https://sistec.mec.gov.br/ws/dadoscpf/cpf/00000000000 - substitui o 0000 pelo cpf e vc acessa a base. Baita vazamento, hein?', 1, 0, 'É um problema de segurança do site do MEC que já foi corrigido.'),
('7aeec1c128183bd9f461652c1f48a287', 1, 'Últimas notícias sobre o Covid19.\n\n\nParece que a doença está sendo atacada em todo o mundo.\n\nGraças às autópsias realizadas pelos italianos ... foi demonstrado que não é pneumonia... mas é: coagulação intravascular disseminada (trombose).  \n\nPortanto, a maneira de combatê-lo é com antibióticos, antivirais…', 1, 1, 'https://www.boatos.org/saude/coronavirus-nao-causa-pneumonia-trombose-respiradores-utis.html'),
('80d7760e386457922fa44a1dfcfa40c0', 2, '', 1, 0, 'Se trata uma divulgação de um edital da rede SibratecNano, publicado no site da rede'),
('858bcf4cdb88cb2f473312aeb8609f86', 1, 'Boas notícias: Informações para todos, o COVID-19 é imune a organismos com um PH maior que 5,5  * VIROLOGY Center, Moscou, Rússia. * Precisamos consumir mais alimentos alcalinos que nos ajudem a aumentar o nível de PH para combater o vírus.  Alguns dos quais são:  Limão .............. 9,9 PH  Abacate ......…', 1, 1, 'https://www.aosfatos.org/noticias/alimentos-alcalinos-nao-ajudam-prevenir-ou-tratar-covid-19/'),
('b0bc1768a5c09a49b451ea374d4f75d8', 3, 'https://l.facebook.com/l.php?u=https%3A%2F%2Frevistaforum.com.br%2Fnoticias%2Fbolsonaro-veta-artigo-que-preve-acesso-a-agua-potavel-na-lei-de-protecao-de-indigenas-contra-coronavirus%2F&h=AT0mtbX8qTAJj1uCwUX25eOLhhiPtEQHLH5NF9eYboVz5s7dyftkLVFk1D7Ai4AxaIFWnMf1WPlQRKagQ55GkozFgUZj4YL74VU761dowNemqRqDNZ2hQ1zLXBOvCigj78QEplQ', 1, 1, 'a publicação foi feita pela Revista Fórum e seu conteúdo é de responsabilidade desse portal de notícias.'),
('c3f7c3a0f652bb4eec05783915e34936', 1, '"Hoje às 22h se vc olhar para o céu, poderá ver o Cometa Halley.\nSua passagem seria só em 2060,  mas foi antecipada por um decreto do governador João Dória."', 1, 1, 'É uma piada, ria!'),
('cce17df93925982c763ddd54f8023c31', 1, 'Informativo do Governo Federal\n\nFamílias que tiveram sua renda afetada pelas políticas de distanciamento social devido a pandemia do novo Coronavírus podem solicitar, a partir de hoje, o benefício do Aluguel Social.\n\nAcesse:\nhttps://cadastrar.beneficio-social.com', 1, 1, 'não clique no link desta mensagem, pois ele irá acessar um vírus e infectar seu aparelho.'),
('d7ae7de3bebf471f802560088279dbdd', 1, 'Recebi isso de um colega medico e achei excelente!!!!\nResumindo:\n1) idoso = isolamento \n2) escolas = é melhor fechar\n3) máscaras = pessoal da área de saúde e pessoas com outras doenças \n4) teste= só em caso suspeito e fazer em casa \n5) hospital = suspeita+ febre alta+ falta de ar\n6) viajante de qualquer lug…', 1, 1, 'https://www.boatos.org/saude/gargarejo-agua-sal-vinagre-cura-coronavirus.html'),
('f3b4dd86d2f288afc7c9aba73204a922', 2, '', 1, 1, 'É uma piada!');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `mensagem`
--
ALTER TABLE `mensagem`
 ADD PRIMARY KEY (`md5`), ADD UNIQUE KEY `md5` (`md5`), ADD KEY `md5_2` (`md5`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
