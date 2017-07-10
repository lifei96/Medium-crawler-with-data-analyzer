function draw_pr()
    dataset = csvread('./data/graph/pagerank.csv', 1, 1);
    h = cdfplot(dataset(:,1));
    xlim([0 1e-5]);
    set(h, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('PageRank','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/graph/CDF_pagerank.eps', '-depsc')
end