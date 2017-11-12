function draw_avg_cc_degree()
    dataset = csvread('./data/graph/avg_cc_degree.csv', 1, 0);
    figure(1);
    h = plot(dataset(:,1), dataset(:,2));
    set(h, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    set(gca,'XScale','log');
    set(gca, 'FontSize', 12);
    xlim([0 100]);
    xlabel('Degree','FontSize',20);
    ylabel('Average clustering coefficient','FontSize',20);
    title('');
    grid off;
    print('./results/graph/avg_cc_degree.eps', '-depsc');